from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

ACTIVE_STATUSES = ["pending", "confirmed"]


class Car(models.Model):
    CATEGORY_CHOICES = [
        ("economy", "Ekonomike"),
        ("suv", "SUV"),
        ("luxury", "Luksoze"),
        ("van", "Familjare / Van"),
    ]
    TRANSMISSION_CHOICES = [
        ("manual", "Manual"),
        ("automatic", "Automatik"),
    ]
    FUEL_CHOICES = [
        ("petrol", "Benzinë"),
        ("diesel", "Naftë"),
        ("hybrid", "Hibrid"),
        ("electric", "Elektrike"),
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
        default=False,
        help_text="Shfaqe këtë makinë edhe në faqen kryesore (index).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.name}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Në pritje"),
        ("confirmed", "Konfirmuar"),
        ("cancelled", "Anuluar"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reservations",
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.full_name} - {self.car}"

    @property
    def days(self):
        if self.pickup_date and self.return_date:
            return max((self.return_date - self.pickup_date).days, 1)
        return 0

    def clean(self):
        super().clean()

        if not (self.pickup_date and self.return_date):
            return

        if self.return_date <= self.pickup_date:
            raise ValidationError("Data e kthimit duhet të jetë pas datës së marrjes.")

        if self._state.adding and self.pickup_date < timezone.localdate():
            raise ValidationError("Data e marrjes nuk mund të jetë në të kaluarën.")

        if self.car_id and self.status in ACTIVE_STATUSES:
            overlap = Reservation.objects.filter(
                car_id=self.car_id,
                status__in=ACTIVE_STATUSES,
                pickup_date__lt=self.return_date,
                return_date__gt=self.pickup_date,
            ).exclude(pk=self.pk)
            if overlap.exists():
                raise ValidationError("Kjo makinë është e zënë në datat e zgjedhura.")

    def save(self, *args, **kwargs):
        if self.car_id:
            self.total_price = self.car.price_per_day * self.days
        super().save(*args, **kwargs)


class Review(models.Model):
    name = models.CharField(max_length=80)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(max_length=600)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}/5)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=2000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

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