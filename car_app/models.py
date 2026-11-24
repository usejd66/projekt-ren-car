import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .images import make_variants

logger = logging.getLogger(__name__)

def default_language():
    return settings.LANGUAGE_CODE


ACTIVE_STATUSES = ("pending", "confirmed")


class Stamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Car(Stamped):
    CATEGORY_CHOICES = [
        ("economy", _("Economy")),
        ("suv", _("SUV")),
        ("luxury", _("Luxury")),
        ("van", _("Family / Van")),
    ]
    TRANSMISSION_CHOICES = [("manual", _("Manual")), ("automatic", _("Automatic"))]
    FUEL_CHOICES = [
        ("petrol", _("Petrol")),
        ("diesel", _("Diesel")),
        ("hybrid", _("Hybrid")),
        ("electric", _("Electric")),
    ]

    brand = models.CharField(max_length=60)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="economy")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default="manual")
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES, default="petrol")
    seats = models.PositiveSmallIntegerField(default=5)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="cars/", blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False, help_text="Shfaqe këtë makinë edhe në faqen kryesore (index)."
    )

    def __str__(self):
        return f"{self.brand} {self.name}"

    @property
    def slug(self):
        return slugify(str(self)) or "car"

    def get_absolute_url(self):
        return reverse("car_detail", args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        _make_variants_safely(self.image)


class CarPhoto(models.Model):
    """Foto shtesë për galerinë e faqes së makinës (shtohen te admin, poshtë makinës)."""

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="cars/")
    order = models.PositiveSmallIntegerField(default=0, help_text="Renditja në galeri (më e vogla del e para).")

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self):
        return f"{self.car} – photo {self.order or self.pk}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        _make_variants_safely(self.image)


def _make_variants_safely(image):
    """Versionet e vogla WebP për faqet (shih images.py); një foto e prishur nuk duhet të ndalë ruajtjen."""
    if not image:
        return
    try:
        make_variants(image.name)
    except (OSError, ValueError):
        logger.exception("Could not create image variants for %s", image.name)


class Reservation(Stamped):
    STATUS_CHOICES = [("pending", "Në pritje"), ("confirmed", "Konfirmuar"), ("cancelled", "Anuluar")]
    MAX_DAYS = 60

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="reservations",
    )
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="reservations")
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    pickup_date = models.DateField()
    return_date = models.DateField()
    pickup_location = models.CharField(max_length=150)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    language = models.CharField(
        max_length=8, default=default_language, editable=False,
        help_text="Gjuha në të cilën u bë rezervimi (emailet e klientit dërgohen në këtë gjuhë).",
    )
    cancel_requested_at = models.DateTimeField(
        null=True, blank=True,
        help_text="Klienti kërkoi anulimin nga 'My bookings'. Vendos ti: ndrysho statusin në 'Anuluar' ose kontakto klientin.",
    )

    def __str__(self):
        return f"#{self.pk} {self.full_name} - {self.car}"

    @property
    def is_upcoming(self):
        return self.status != "cancelled" and self.return_date >= timezone.localdate()

    @property
    def can_cancel(self):
        """Klienti mund të anulojë/kërkojë anulim vetëm para datës së marrjes."""
        return self.status in ACTIVE_STATUSES and self.pickup_date > timezone.localdate() and not self.cancel_requested_at

    @property
    def days(self):
        if self.pickup_date and self.return_date:
            return (self.return_date - self.pickup_date).days
        return 0

    @classmethod
    def overlapping(cls, car_id, start, end, exclude_pk=None):
        """Rezervimet aktive që prekin [start, end]. Skajet përfshihen (dita e kthimit është e zënë)."""
        return cls.objects.filter(
            car_id=car_id, status__in=ACTIVE_STATUSES,
            pickup_date__lte=end, return_date__gte=start,
        ).exclude(pk=exclude_pk)

    def clean(self):
        if not (self.pickup_date and self.return_date):
            return
        if self.return_date <= self.pickup_date:
            raise ValidationError(_("The return date must be after the pickup date."))
        if self._state.adding and self.pickup_date < timezone.localdate():
            raise ValidationError(_("The pickup date cannot be in the past."))
        if self.days > self.MAX_DAYS:
            raise ValidationError(_("A reservation cannot be longer than %(days)s days.") % {"days": self.MAX_DAYS})
        if (
            self.car_id
            and self.status in ACTIVE_STATUSES
            and self.overlapping(self.car_id, self.pickup_date, self.return_date, self.pk).exists()
        ):
            raise ValidationError(_("This car is already booked on the selected dates."))

    def save(self, *args, **kwargs):
        if self.car_id:
            self.total_price = self.car.price_per_day * self.days
        super().save(*args, **kwargs)


class Review(Stamped):
    name = models.CharField(max_length=80)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(max_length=600)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.rating}/5)"


class ContactMessage(Stamped):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=2000)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.subject}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email

class Lead(models.Model):
    """Një "kontakt" nga faqja: rezervim, klikim në WhatsApp/telefon/email ose mesazh nga Contact.

    Këto numra tregojnë sa klientë sjell faqja (shih admin → Results dhe raportin mujor).
    """

    KIND_CHOICES = [
        ("booking", "Rezervim"),
        ("whatsapp", "Klikim WhatsApp"),
        ("phone", "Klikim telefon"),
        ("email", "Klikim email"),
        ("contact", "Mesazh nga Contact"),
    ]
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    source = models.CharField(max_length=40, default="direct", help_text="Nga erdhi vizitori: google, instagram, facebook, direct...")
    page = models.CharField(max_length=200, blank=True, help_text="Faqja ku ndodhi")
    reservation = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.SET_NULL, related_name="leads")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "kontakt"
        verbose_name_plural = "📈 Rezultatet (klientët nga faqja)"

    def __str__(self):
        return f"{self.get_kind_display()} · {self.source} · {self.created_at:%d/%m/%Y %H:%M}"
