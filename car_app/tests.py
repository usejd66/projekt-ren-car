from datetime import timedelta

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from .admin import ReservationAdmin
from .models import Car, Reservation


class BaseCase(TestCase):
    def setUp(self):
        self.car = Car.objects.create(brand="Audi", name="A4", price_per_day=50)
        self.today = timezone.localdate()

    def book(self, start, end, **extra):
        return Reservation.objects.create(
            car=self.car, full_name="Test User", email="t@t.al", phone="+355690000000",
            pickup_date=self.today + timedelta(days=start),
            return_date=self.today + timedelta(days=end),
            pickup_location="Tirana", **extra,
        )

    def post_reservation(self, start, end):
        return self.client.post(reverse("reservation"), {
            "car": self.car.pk, "full_name": "Ana Hoxha", "email": "ana@test.al",
            "phone": "+355 69 123 4567",
            "pickup_date": (self.today + timedelta(days=start)).isoformat(),
            "return_date": (self.today + timedelta(days=end)).isoformat(),
            "pickup_location": "Tirana",
        })


class PagesTest(BaseCase):
    def test_pages_load(self):
        for name in ["index", "about", "cars", "explorefleet", "contact", "reservation", "signup", "login"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)


class ReservationTest(BaseCase):
    def test_valid_reservation_computes_total(self):
        self.post_reservation(1, 4)
        r = Reservation.objects.get()
        self.assertEqual(r.total_price, 150)

    def test_overlap_is_rejected(self):
        self.book(2, 5)
        self.post_reservation(4, 7)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_past_date_is_rejected(self):
        self.post_reservation(-1, 2)
        self.assertFalse(Reservation.objects.exists())

    def test_longer_than_max_days_is_rejected(self):
        self.post_reservation(1, Reservation.MAX_DAYS + 2)
        self.assertFalse(Reservation.objects.exists())


class AdminConfirmTest(BaseCase):
    def run_confirm(self, queryset):
        request = RequestFactory().post("/")
        request.user = get_user_model().objects.create_superuser("admin", "a@a.al", "pass")
        request.session = {}
        request._messages = FallbackStorage(request)
        ReservationAdmin(Reservation, AdminSite()).confirm_reservations(request, queryset)

    def test_cancelled_overlapping_is_not_confirmed(self):
        self.book(1, 3, status="confirmed")
        cancelled = Reservation.objects.create(
            car=self.car, full_name="Old", email="o@o.al", phone="+355690000001",
            pickup_date=self.today + timedelta(days=2), return_date=self.today + timedelta(days=4),
            pickup_location="Tirana", status="cancelled",
        )
        self.run_confirm(Reservation.objects.filter(pk=cancelled.pk))
        cancelled.refresh_from_db()
        self.assertEqual(cancelled.status, "cancelled")

    def test_pending_is_confirmed(self):
        r = self.book(1, 3)
        self.run_confirm(Reservation.objects.filter(pk=r.pk))
        r.refresh_from_db()
        self.assertEqual(r.status, "confirmed")
