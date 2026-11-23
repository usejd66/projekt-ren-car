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


class PwaTest(TestCase):
    def test_manifest(self):
        r = self.client.get(reverse("manifest"))
        self.assertEqual(r["Content-Type"], "application/manifest+json")
        data = r.json()
        self.assertEqual(data["short_name"], "DriveOn")
        self.assertTrue(any(i["sizes"] == "512x512" for i in data["icons"]))

    def test_service_worker_and_offline_page(self):
        sw = self.client.get(reverse("service_worker"))
        self.assertEqual(sw["Content-Type"], "application/javascript")
        self.assertContains(sw, '"/offline/"')
        self.assertIn("no-cache", sw["Cache-Control"])
        self.assertContains(self.client.get(reverse("offline")), "You're offline")

    def test_sw_registered_only_in_production(self):
        with self.settings(DEBUG=True):
            self.assertNotContains(self.client.get(reverse("index")), "serviceWorker")
        with self.settings(DEBUG=False):
            self.assertContains(self.client.get(reverse("index")), "serviceWorker")


class CarDetailTest(BaseCase):
    def test_page_shows_car_price_and_structured_data(self):
        r = self.client.get(self.car.get_absolute_url())
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "<h1>Audi A4</h1>", html=True)
        self.assertContains(r, '"@type": "Car"')
        self.assertContains(r, "Continue to booking")

    def test_wrong_slug_redirects_and_keeps_dates(self):
        r = self.client.get(f"/cars/{self.car.pk}/old-name/?pickup_date=2030-01-01")
        self.assertRedirects(r, self.car.get_absolute_url() + "?pickup_date=2030-01-01",
                             status_code=301, fetch_redirect_response=False)

    def test_booked_dates_and_similar_cars(self):
        self.book(2, 5)
        same = Car.objects.create(brand="BMW", name="3 Series", price_per_day=60, category=self.car.category)
        Car.objects.create(brand="Fiat", name="Ducato", price_per_day=80, category="van")
        r = self.client.get(self.car.get_absolute_url())
        start = (self.today + timedelta(days=2)).isoformat()
        self.assertContains(r, f'"from": "{start}"')
        self.assertEqual(list(r.context["similar"]), [same])

    def test_unavailable_car_cannot_be_booked(self):
        self.car.is_available = False
        self.car.save()
        r = self.client.get(self.car.get_absolute_url())
        self.assertContains(r, "Currently unavailable")
        self.assertNotContains(r, "Continue to booking")

    def test_missing_car_is_404(self):
        self.assertEqual(self.client.get("/cars/9999/nothing/").status_code, 404)

    def test_tiles_link_to_detail_page(self):
        self.car.is_featured = True
        self.car.save()
        self.assertContains(self.client.get(reverse("index")), self.car.get_absolute_url())
        self.assertContains(self.client.get(reverse("cars")), self.car.get_absolute_url())


class EmailTest(BaseCase):
    def setUp(self):
        super().setUp()
        from django.core import mail
        self.mail = mail

    def test_booking_sends_customer_and_owner_emails(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.post_reservation(1, 4)
        booking = Reservation.objects.get()
        self.assertEqual(len(self.mail.outbox), 2)
        customer, owner = self.mail.outbox
        self.assertEqual(customer.to, ["ana@test.al"])
        self.assertIn(f"#{booking.pk}", customer.subject)
        self.assertIn("€150", customer.body)
        self.assertIn("€150", customer.alternatives[0][0])  # versioni HTML
        self.assertEqual(owner.reply_to, ["ana@test.al"])
        self.assertIn(f"/admin/car_app/reservation/{booking.pk}/change/", owner.body)

    def test_text_email_is_not_html_escaped(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("reservation"), {
                "car": self.car.pk, "full_name": "Ana & Ben Hoxha", "email": "ana@test.al",
                "phone": "+355 69 123 4567",
                "pickup_date": (self.today + timedelta(days=1)).isoformat(),
                "return_date": (self.today + timedelta(days=3)).isoformat(),
                "pickup_location": "Tirana",
            })
        self.assertIn("Hi Ana & Ben Hoxha", self.mail.outbox[0].body)

    def test_admin_confirm_and_cancel_notify_customer(self):
        r = self.book(1, 3)
        admin_test = AdminConfirmTest()
        with self.captureOnCommitCallbacks(execute=True):
            AdminConfirmTest.run_confirm(admin_test, Reservation.objects.filter(pk=r.pk))
        self.assertEqual(len(self.mail.outbox), 1)
        self.assertIn("is confirmed", self.mail.outbox[0].subject)

    def test_contact_form_notifies_owner(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("contact"), {
                "name": "Arben", "email": "arben@test.al", "subject": "Airport pickup", "message": "Hi, is it possible?",
            })
        self.assertEqual(len(self.mail.outbox), 1)
        self.assertEqual(self.mail.outbox[0].reply_to, ["arben@test.al"])

    def test_failed_email_does_not_break_booking(self):
        from unittest import mock
        with mock.patch("django.core.mail.EmailMultiAlternatives.send", side_effect=OSError("SMTP down")):
            # assertLogs jashtë: emailet dërgohen kur mbyllet captureOnCommitCallbacks
            with self.assertLogs("car_app.emails", "ERROR"), self.captureOnCommitCallbacks(execute=True):
                r = self.post_reservation(1, 4)
        self.assertRedirects(r, reverse("reservation_success"))
        self.assertEqual(Reservation.objects.count(), 1)
