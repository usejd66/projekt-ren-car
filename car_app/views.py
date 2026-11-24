import hashlib
from urllib.parse import urlparse
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count, DecimalField, ExpressionWrapper, F, Min, Q
from django.http import Http404, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.templatetags.static import static
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import slugify
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import branding, emails
from .forms import LOCATIONS, ContactForm, ReservationForm, SignUpForm, SubscribeForm
from .models import ACTIVE_STATUSES, Car, Lead, Reservation, Review


SORT_OPTIONS = {
    "newest": "-created_at",
    "price_asc": "price_per_day",
    "price_desc": "-price_per_day",
}


def _parse_trip(get):
    """Vendi dhe datat nga formulari i kërkimit (?pickup_location=&pickup_date=&return_date=).

    Kthen {"location", "start", "end", "days", "error"}; "start"/"end" janë None nëse
    datat mungojnë ose nuk janë të vlefshme.
    """
    location = get.get("pickup_location", "")
    trip = {
        "location": location if location in LOCATIONS else "",
        "start": None, "end": None, "days": 0, "error": "",
    }
    raw_start, raw_end = get.get("pickup_date", ""), get.get("return_date", "")
    if not (raw_start or raw_end):
        return trip
    try:
        start, end = date.fromisoformat(raw_start), date.fromisoformat(raw_end)
    except ValueError:
        trip["error"] = _("Please choose both a pickup and a return date.")
        return trip
    if start < timezone.localdate():
        trip["error"] = _("The pickup date cannot be in the past.")
    elif end <= start:
        trip["error"] = _("The return date must be after the pickup date.")
    elif (end - start).days > Reservation.MAX_DAYS:
        trip["error"] = _("A rental cannot be longer than %(days)s days.") % {"days": Reservation.MAX_DAYS}
    else:
        trip.update(start=start, end=end, days=(end - start).days)
    return trip


def _query_without(get, *keys):
    """Query string-u aktual pa çelësat e dhënë (për linket e filtrave dhe faqosjes)."""
    params = get.copy()
    for key in keys:
        params.pop(key, None)
    return params.urlencode()


def _filtered_cars(request):
    """Filtrimi, disponueshmëria sipas datave dhe paginimi i makinave."""
    get = request.GET

    q = get.get("q", "").strip()
    category = get.get("category", "")
    transmission = get.get("transmission", "")
    max_price = get.get("max_price", "")
    sort = get.get("sort", "newest")
    trip = _parse_trip(get)

    cars = Car.objects.filter(is_available=True)

    if q:
        cars = cars.filter(
            Q(name__icontains=q) | Q(brand__icontains=q)
        )

    if category in dict(Car.CATEGORY_CHOICES):
        cars = cars.filter(category=category)

    if transmission in dict(Car.TRANSMISSION_CHOICES):
        cars = cars.filter(transmission=transmission)

    if max_price.isdigit():
        cars = cars.filter(price_per_day__lte=int(max_price))

    if trip["start"]:
        # vetëm makinat pa rezervim aktiv që prek këto data
        booked = Reservation.objects.filter(
            status__in=ACTIVE_STATUSES,
            pickup_date__lte=trip["end"],
            return_date__gte=trip["start"],
        ).values("car_id")
        cars = cars.exclude(pk__in=booked).annotate(
            trip_total=ExpressionWrapper(
                F("price_per_day") * trip["days"],
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )

    page = Paginator(
        cars.order_by(SORT_OPTIONS.get(sort, "-created_at")), 9
    ).get_page(get.get("page"))

    # parametrat që i kalohen faqes së rezervimit kur shtyp "Rent Now"
    book_params = QueryDict(mutable=True)
    if trip["location"]:
        book_params["pickup_location"] = trip["location"]
    if trip["start"]:
        book_params["pickup_date"] = trip["start"].isoformat()
        book_params["return_date"] = trip["end"].isoformat()

    return {
        "page_obj": page,
        "cars": page.object_list,
        "categories": Car.CATEGORY_CHOICES,
        "transmissions": Car.TRANSMISSION_CHOICES,
        "locations": LOCATIONS,
        "trip": trip,
        "qs_no_page": _query_without(get, "page"),
        "qs_no_category": _query_without(get, "page", "category"),
        "book_qs": book_params.urlencode(),
        # sa filtra janë aktivë (për butonin "Filters (2)" në telefon)
        "active_filters": sum(bool(v) for v in (q, transmission, max_price)) + (sort != "newest"),
        "filters": {
            "q": q,
            "category": category,
            "transmission": transmission,
            "max_price": max_price,
            "sort": sort,
        },
    }


def _booked_ranges(cars):
    """{car_id: [{"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}, ...]} për rezervimet aktive nga sot e tutje."""
    booked = {}
    rows = Reservation.objects.filter(
        car__in=cars,
        status__in=ACTIVE_STATUSES,
        return_date__gte=timezone.localdate(),
    ).order_by("pickup_date").values_list("car_id", "pickup_date", "return_date")
    for car_id, start, end in rows:
        booked.setdefault(car_id, []).append({"from": start.isoformat(), "to": end.isoformat()})
    return booked


def car_detail(request, pk, slug):
    car = get_object_or_404(Car.objects.prefetch_related("photos"), pk=pk)
    if slug != car.slug:  # emri ndryshoi ose URL e shkruar gabim: ridrejto te URL-ja e saktë
        query = f"?{request.GET.urlencode()}" if request.GET else ""
        return redirect(car.get_absolute_url() + query, permanent=True)

    trip = _parse_trip(request.GET)
    similar = (
        Car.objects.filter(is_available=True, category=car.category)
        .exclude(pk=car.pk).order_by("price_per_day")[:3]
    )
    return render(request, "car_detail.html", {
        "car": car,
        "photos": list(car.photos.all()),
        "booked": _booked_ranges([car]).get(car.pk, []),
        "trip": trip,
        "locations": LOCATIONS,
        "similar": similar,
    })


def index(request):
    approved = Review.objects.filter(is_approved=True)
    stats = approved.aggregate(
        avg=Avg("rating"),
        total=Count("id"),
    )
    available = Car.objects.filter(is_available=True)
    counts = dict(
        available.values_list("category").annotate(n=Count("id")).values_list("category", "n")
    )

    return render(request, "index.html", {
        "featured_cars": available.filter(is_featured=True)[:4],
        "min_price": available.aggregate(m=Min("price_per_day"))["m"],
        "categories": [
            {"key": key, "label": label, "count": counts.get(key, 0)}
            for key, label in Car.CATEGORY_CHOICES
        ],
        "locations": LOCATIONS,
        "reviews": approved[:3],
        "rating_avg": round(stats["avg"] or 0, 1),
        "rating_total": stats["total"],
    })


def about(request):
    return render(request, "about.html")


def cars(request):
    return render(request, "cars.html", _filtered_cars(request))


def explore_fleet(request):
    # faqja e vjetër me makina të shkruara me dorë: tani lista reale është te Cars
    return redirect("cars", permanent=True)


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        emails.contact_message(form.save())
        Lead.objects.create(kind="contact", source=request.session.get("src", "direct"), page=request.path)
        messages.success(
            request,
            _("Thank you! Your message has been sent. We'll get back to you shortly."),
        )
        return redirect("contact")

    return render(request, "contact.html", {"form": form})


def reservation(request):
    user = request.user
    initial = {"car": request.GET.get("car")}

    # Nga formulari i kërkimit në faqen kryesore: plotëso vendin dhe datat
    if request.GET.get("pickup_location") in LOCATIONS:
        initial["pickup_location"] = request.GET["pickup_location"]
    for field in ("pickup_date", "return_date"):
        try:
            # si tekst "YYYY-MM-DD": template-i e vendos direkt te input-i i kalendarit
            initial[field] = date.fromisoformat(request.GET.get(field, "")).isoformat()
        except ValueError:
            pass

    if user.is_authenticated:
        initial.update({
            "full_name": user.get_full_name() or user.username,
            "email": user.email,
        })

    form = ReservationForm(
        request.POST or None,
        initial=initial,
    )

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        with transaction.atomic():
            car = Car.objects.select_for_update().get(
                pk=data["car"].pk
            )

            if Reservation.overlapping(
                car.pk,
                data["pickup_date"],
                data["return_date"],
            ).exists():
                form.add_error(
                    None,
                    _("This car was just booked for the selected dates. Please choose different dates."),
                )
            else:
                booking = form.save(commit=False)
                booking.user = user if user.is_authenticated else None
                booking.language = get_language() or settings.LANGUAGE_CODE
                booking.save()

                emails.booking_received(booking)
                Lead.objects.create(kind="booking", reservation=booking,
                                    source=request.session.get("src", "direct"), page=request.path)
                # faqja e konfirmimit e shfaq vetëm rezervimin e këtij vizitori
                request.session["last_booking"] = booking.pk
                return redirect("reservation_success")

    cars_qs = Car.objects.filter(
        is_available=True
    ).order_by("category", "name")

    return render(request, "reservation.html", {
        "form": form,
        "cars": cars_qs,
        "booked": _booked_ranges(cars_qs),
    })


def reservation_success(request):
    booking = (
        Reservation.objects.select_related("car")
        .filter(pk=request.session.get("last_booking"))
        .first()
    )
    if booking is None:
        return redirect("reservation")
    return render(request, "reservation_success.html", {"booking": booking})


@login_required
def my_bookings(request):
    bookings = list(request.user.reservations.select_related("car").order_by("-pickup_date"))
    return render(request, "my_bookings.html", {
        "upcoming": sorted([b for b in bookings if b.is_upcoming], key=lambda b: b.pickup_date),
        "past": [b for b in bookings if not b.is_upcoming],
    })


@login_required
@require_POST
def cancel_booking(request, pk):
    booking = get_object_or_404(Reservation, pk=pk, user=request.user)  # vetëm rezervimet e veta
    if not booking.can_cancel:
        messages.error(request, _("This booking can no longer be cancelled online. Please contact us."))
    elif booking.status == "pending":
        # ende i pakonfirmuar: anulohet menjëherë, datat lirohen
        booking.status = "cancelled"
        booking.save(update_fields=["status"])
        emails.booking_cancelled_by_customer(booking, requested=False)
        messages.success(request, _("Booking #%(n)s has been cancelled.") % {"n": booking.pk})
    else:
        # i konfirmuar: kërkesë që e shqyrton pronari
        booking.cancel_requested_at = timezone.now()
        booking.save(update_fields=["cancel_requested_at"])
        emails.booking_cancelled_by_customer(booking, requested=True)
        messages.success(request, _("Your cancellation request was sent. We'll contact you shortly."))
    return redirect("my_bookings")


def location_page(request, slug):
    """Faqe për çdo vend marrjeje (p.sh. /rent-a-car/tirana-airport/) – për kërkimet në Google."""
    location = next((loc for loc in LOCATIONS if slugify(loc) == slug), None)
    if location is None:
        raise Http404
    available = Car.objects.filter(is_available=True)
    return render(request, "location.html", {
        "location": location,
        "is_airport": "airport" in location.lower(),
        "cars": available.order_by("price_per_day")[:6],
        "min_price": available.aggregate(m=Min("price_per_day"))["m"],
        "locations": LOCATIONS,
        "trip": {"location": location},
    })


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /account/",
        "Disallow: /reservation/success/",
        "Disallow: /t/",
        f"Sitemap: {request.scheme}://{request.get_host()}{reverse('django.contrib.sitemaps.views.sitemap')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def rental_terms(request):
    return render(request, "rental_terms.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                _("Your account has been created. Welcome to %(name)s!") % {"name": branding.BRAND["name"]},
            )
            return redirect("index")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                _("Thank you! You are now subscribed to our newsletter."),
            )
        else:
            email_errors = form.errors.get("email")

            if email_errors:
                messages.error(request, email_errors[0])

    back = request.META.get("HTTP_REFERER", "")

    if back and url_has_allowed_host_and_scheme(
        back,
        allowed_hosts={request.get_host()},
    ):
        return redirect(back)

    return redirect("index")


# ===== PWA: manifest, service worker, faqja pa internet =====

def manifest(request):
    """Manifesti i aplikacionit: lejon "Add to Home Screen" në telefon."""
    brand = branding.site()
    return JsonResponse({
        "name": f"{brand['name']} – Car Rental in {brand['city']}",
        "short_name": brand["name"],
        "description": f"Rent a car in {brand['locations_text']}.",
        "start_url": "/?source=pwa",
        "scope": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": brand["color"],
        "icons": [
            {"src": static("image/apple-touch-icon.png"), "sizes": "180x180", "type": "image/png"},
            {"src": static("image/icon-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }, content_type="application/manifest+json")


SW_PRECACHE = ("css/style.css", "css/responsive.css", "icons.svg", "js/script.js", "image/favicon-32.png")


@cache_control(no_cache=True)  # shfletuesi duhet ta kontrollojë gjithmonë për versione të reja
def service_worker(request):
    urls = ["/offline/"] + [static(path) for path in SW_PRECACHE]
    version = hashlib.md5("|".join(urls).encode()).hexdigest()[:10]
    return render(request, "sw.js", {"urls": urls, "version": version},
                  content_type="application/javascript")


def offline(request):
    return render(request, "offline.html")


# ===== Matja: klikimet në WhatsApp / telefon / email (dërgohen nga script.js me sendBeacon) =====

TRACKED_CLICKS = {"whatsapp", "phone", "email"}


@csrf_exempt  # sendBeacon nuk dërgon token CSRF; pranojmë vetëm tre lloje dhe vetëm nga e njëjta faqe
@require_POST
def track(request):
    kind = request.POST.get("kind", "")
    origin = urlparse(request.headers.get("Origin") or request.headers.get("Referer") or "").netloc
    if kind not in TRACKED_CLICKS or origin != request.get_host():
        return HttpResponse(status=400)
    # mos numëro dy herë të njëjtin klikim (p.sh. dy prekje rresht)
    key = f"t_{kind}"
    now = int(timezone.now().timestamp())
    if now - request.session.get(key, 0) < 30:
        return HttpResponse(status=204)
    request.session[key] = now
    page = urlparse(request.headers.get("Referer", "")).path[:200]
    Lead.objects.create(kind=kind, source=request.session.get("src", "direct"), page=page)
    return HttpResponse(status=204)
