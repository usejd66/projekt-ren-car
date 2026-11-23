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
        for name in ["index", "about", "cars", "contact", "reservation", "signup", "login"]:
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


class TripSearchTest(BaseCase):
    def search(self, start, end, **extra):
        return self.client.get(reverse("cars"), {
            "pickup_location": "Durrës",
            "pickup_date": (self.today + timedelta(days=start)).isoformat(),
            "return_date": (self.today + timedelta(days=end)).isoformat(),
            **extra,
        })

    def test_booked_car_is_hidden_and_free_car_shows_total(self):
        free = Car.objects.create(brand="Toyota", name="Yaris", price_per_day=30)
        self.book(2, 5)  # self.car (Audi A4) është i zënë
        r = self.search(3, 6)
        cars = list(r.context["cars"])
        self.assertEqual(cars, [free])
        self.assertEqual(cars[0].trip_total, 90)
        self.assertContains(r, "€90")

    def test_car_is_available_outside_booked_dates(self):
        self.book(2, 5)
        r = self.search(6, 8)
        self.assertEqual(list(r.context["cars"]), [self.car])

    def test_invalid_dates_show_error_and_do_not_filter(self):
        self.book(2, 5)
        r = self.search(5, 3)
        self.assertContains(r, "The return date must be after the pickup date.")
        self.assertEqual(list(r.context["cars"]), [self.car])

    def test_rent_link_and_filters_keep_trip(self):
        r = self.search(3, 6, transmission="manual")
        start = (self.today + timedelta(days=3)).isoformat()
        self.assertIn(f"pickup_date={start}", r.context["book_qs"])
        self.assertIn(f"pickup_date={start}", r.context["qs_no_page"])
        self.assertIn("transmission=manual", r.context["qs_no_category"])
        self.assertNotIn("category=", r.context["qs_no_category"].replace("transmission", ""))


class ReservationPrefillTest(BaseCase):
    def test_search_prefills_reservation(self):
        start = (self.today + timedelta(days=3)).isoformat()
        end = (self.today + timedelta(days=6)).isoformat()
        r = self.client.get(reverse("reservation"), {
            "pickup_location": "Durrës", "pickup_date": start, "return_date": end,
        })
        self.assertContains(r, f'value="{start}"')
        self.assertContains(r, f'value="{end}"')
        self.assertContains(r, '<option value="Durrës" selected>')

    def test_bad_values_are_ignored(self):
        r = self.client.get(reverse("reservation"), {"pickup_location": "Mars", "pickup_date": "abc"})
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'value="Mars"')


class ReservationSuccessTest(BaseCase):
    def test_success_page_shows_own_booking(self):
        r = self.post_reservation(1, 4)
        self.assertRedirects(r, reverse("reservation_success"))
        page = self.client.get(reverse("reservation_success"))
        self.assertContains(page, "Reservation received")
        self.assertContains(page, "€150")

    def test_success_page_without_booking_redirects(self):
        self.book(1, 3)  # rezervim i dikujt tjetër
        r = self.client.get(reverse("reservation_success"))
        self.assertRedirects(r, reverse("reservation"))

    def test_invalid_field_is_highlighted(self):
        r = self.client.post(reverse("reservation"), {"car": self.car.pk, "phone": "abc"})
        self.assertContains(r, "is-invalid")
        self.assertContains(r, "Please enter a valid phone number.")


class CarImageTest(TestCase):
    """Fotot e makinave marrin automatikisht versione WebP (në një dosje të përkohshme)."""

    def setUp(self):
        import shutil
        import tempfile
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, ignore_errors=True)
        self.override = self.settings(MEDIA_ROOT=self.media)
        self.override.enable()
        self.addCleanup(self.override.disable)

    def make_car(self):
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image

        buf = BytesIO()
        Image.new("RGB", (2400, 1600), (200, 30, 40)).save(buf, "JPEG")
        upload = SimpleUploadedFile("photo.jpg", buf.getvalue(), content_type="image/jpeg")
        return Car.objects.create(brand="Audi", name="A6", price_per_day=70, image=upload, is_featured=True)

    def test_variants_are_created_on_save(self):
        from django.core.files.storage import default_storage

        from .images import SIZES, variant_name

        car = self.make_car()
        for w in SIZES:
            name = variant_name(car.image.name, w)
            self.assertTrue(default_storage.exists(name), name)
        from PIL import Image
        with default_storage.open(variant_name(car.image.name, 480)) as f:
            self.assertEqual(Image.open(f).size, (480, 320))

    def test_pages_use_srcset(self):
        self.make_car()
        r = self.client.get(reverse("index"))
        self.assertContains(r, 'srcset="')
        self.assertContains(r, "-480.webp 480w")
