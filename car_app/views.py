from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ContactForm, ReservationForm, SignUpForm, SubscribeForm
from .models import ACTIVE_STATUSES, Car, Review, Reservation

SORT_OPTIONS = {
    "newest": "-created_at",
    "price_asc": "price_per_day",
    "price_desc": "-price_per_day",
}


def _filtered_cars(request):
    """Filtrimi i përbashkët për cars.html dhe explorefleet.html."""
    cars = Car.objects.filter(is_available=True)

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    transmission = request.GET.get("transmission", "")
    max_price = request.GET.get("max_price", "")
    sort = request.GET.get("sort", "newest")

    if q:
        cars = cars.filter(Q(name__icontains=q) | Q(brand__icontains=q))
    if category in dict(Car.CATEGORY_CHOICES):
        cars = cars.filter(category=category)
    if transmission in dict(Car.TRANSMISSION_CHOICES):
        cars = cars.filter(transmission=transmission)
    if max_price.isdigit():
        cars = cars.filter(price_per_day__lte=int(max_price))

    cars = cars.order_by(SORT_OPTIONS.get(sort, "-created_at"))

    page = Paginator(cars, 9).get_page(request.GET.get("page"))

    return {
        "page_obj": page,
        "cars": page.object_list,
        "categories": Car.CATEGORY_CHOICES,
        "transmissions": Car.TRANSMISSION_CHOICES,
        "filters": {
            "q": q,
            "category": category,
            "transmission": transmission,
            "max_price": max_price,
            "sort": sort,
        },
    }


def index(request):
    approved = Review.objects.filter(is_approved=True)
    stats = approved.aggregate(avg=Avg("rating"), total=Count("id"))

    context = {
        "featured_cars": Car.objects.filter(is_available=True, is_featured=True)[:6],
        "reviews": approved[:6],
        "rating_avg": round(stats["avg"] or 0, 1),
        "rating_total": stats["total"],
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def cars(request):
    context = _filtered_cars(request)
    context["reviews"] = Review.objects.filter(is_approved=True)[:6]
    return render(request, "cars.html", context)


def explore_fleet(request):
    return render(request, "explorefleet.html", _filtered_cars(request))


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesazhi u dërgua. Do t'ju përgjigjemi sa më shpejt.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def reservation(request):
    initial = {}
    car_id = request.GET.get("car", "")
    if car_id.isdigit():
        initial["car"] = int(car_id)

    if request.user.is_authenticated:
        initial.setdefault("full_name", request.user.get_full_name() or request.user.username)
        initial.setdefault("email", request.user.email)

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            messages.success(
                request,
                f"Rezervimi #{booking.pk} u regjistrua. Totali: {booking.total_price} € "
                f"për {booking.days} ditë.",
            )
            return redirect("reservation")
    else:
        form = ReservationForm(initial=initial)

    return render(request, "reservation.html", {"form": form})


def car_availability(request, car_id):
    """Për reservation.js: çmimi për ditë dhe datat e zëna të makinës."""
    car = get_object_or_404(Car, pk=car_id, is_available=True)

    booked = Reservation.objects.filter(
        car=car,
        status__in=ACTIVE_STATUSES,
        return_date__gte=timezone.localdate(),
    ).values_list("pickup_date", "return_date")

    return JsonResponse(
        {
            "price_per_day": str(car.price_per_day),
            "booked": [{"from": a.isoformat(), "to": b.isoformat()} for a, b in booked],
        }
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Llogaria u krijua. Mirë se vini!")
            return redirect("index")
    else:
        form = SignUpForm()

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