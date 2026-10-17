from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LOCATIONS, ContactForm, ReservationForm, SignUpForm, SubscribeForm
from .models import ACTIVE_STATUSES, Car, Reservation, Review

SORT_OPTIONS = {"newest": "-created_at", "price_asc": "price_per_day", "price_desc": "-price_per_day"}


def _filtered_cars(request):
    """Filtrimi i përbashkët për cars.html dhe explorefleet.html."""
    get = request.GET
    q, category, transmission = get.get("q", "").strip(), get.get("category", ""), get.get("transmission", "")
    max_price, sort = get.get("max_price", ""), get.get("sort", "newest")

    cars = Car.objects.filter(is_available=True)
    if q:
        cars = cars.filter(Q(name__icontains=q) | Q(brand__icontains=q))
    if category in dict(Car.CATEGORY_CHOICES):
        cars = cars.filter(category=category)
    if transmission in dict(Car.TRANSMISSION_CHOICES):
        cars = cars.filter(transmission=transmission)
    if max_price.isdigit():
        cars = cars.filter(price_per_day__lte=int(max_price))

    page = Paginator(cars.order_by(SORT_OPTIONS.get(sort, "-created_at")), 9).get_page(get.get("page"))
    return {
        "page_obj": page,
        "cars": page.object_list,
        "categories": Car.CATEGORY_CHOICES,
        "transmissions": Car.TRANSMISSION_CHOICES,
        "filters": {"q": q, "category": category, "transmission": transmission,
                    "max_price": max_price, "sort": sort},
    }


def index(request):
    approved = Review.objects.filter(is_approved=True)
    stats = approved.aggregate(avg=Avg("rating"), total=Count("id"))
    return render(request, "index.html", {
        "featured_cars": Car.objects.filter(is_available=True, is_featured=True)[:6],
        "reviews": approved[:6],
        "rating_avg": round(stats["avg"] or 0, 1),
        "rating_total": stats["total"],
    })


def about(request):
    return render(request, "about.html")


def cars(request):
    context = _filtered_cars(request)
    context["reviews"] = Review.objects.filter(is_approved=True)[:6]
    return render(request, "cars.html", context)


def explore_fleet(request):
    return render(request, "explorefleet.html", _filtered_cars(request))


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Mesazhi u dërgua. Do t'ju përgjigjemi sa më shpejt.")
        return redirect("contact")
    return render(request, "contact.html", {"form": form})


def reservation(request):
    user = request.user
    initial = {"car": request.GET.get("car")}  # Rent Now -> ?car=<id>
    if user.is_authenticated:
        initial |= {"full_name": user.get_full_name() or user.username, "email": user.email}

    form = ReservationForm(request.POST or None, initial=initial)
    if form.is_valid():
        data = form.cleaned_data
        with transaction.atomic():
            # Kyç rreshtin e makinës: dy kërkesa njëkohësisht nuk mund ta rezervojnë të njëjtën makinë.
            car = Car.objects.select_for_update().get(pk=data["car"].pk)
            if Reservation.overlapping(car.pk, data["pickup_date"], data["return_date"]).exists():
                form.add_error(None, "Kjo makinë sapo u zu në datat e zgjedhura. Zgjidhni data të tjera.")
            else:
                booking = form.save(commit=False)
                booking.user = user if user.is_authenticated else None
                booking.save()
                messages.success(request, f"Rezervimi u regjistrua. Totali: €{booking.total_price}")
                return redirect("reservation")

    cars_qs = Car.objects.filter(is_available=True).order_by("category", "name")
    booked = {}  # {car_id: [{"from": iso, "to": iso}, ...]} për kalendarin
    rows = Reservation.objects.filter(
        car__in=cars_qs, status__in=ACTIVE_STATUSES, return_date__gte=timezone.localdate()
    ).order_by("pickup_date").values_list("car_id", "pickup_date", "return_date")
    for car_id, start, end in rows:
        booked.setdefault(car_id, []).append({"from": start.isoformat(), "to": end.isoformat()})

    return render(request, "reservation.html",
                  {"form": form, "cars": cars_qs, "booked": booked, "locations": LOCATIONS})


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, "Llogaria u krijua. Mirë se vini!")
        return redirect("index")
    return render(request, "signup.html", {"form": form})


def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Faleminderit! U abonuat me sukses.")
        else:
            messages.error(request, form.errors["email"][0])

    back = request.META.get("HTTP_REFERER", "")
    if back and url_has_allowed_host_and_scheme(back, allowed_hosts={request.get_host()}):
        return redirect(back)
    return redirect("index")