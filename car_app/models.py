from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

ACTIVE_STATUSES = ("pending", "confirmed")


class Stamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Car(Stamped):
    CATEGORY_CHOICES = [
        ("economy", "Ekonomike"),
        ("suv", "SUV"),
        ("luxury", "Luksoze"),
        ("van", "Familjare / Van"),
    ]
    TRANSMISSION_CHOICES = [("manual", "Manual"), ("automatic", "Automatik")]
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
        default=False, help_text="Shfaqe këtë makinë edhe në faqen kryesore (index)."
    )

    def __str__(self):
        return f"{self.brand} {self.name}"


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

    def __str__(self):
        return f"#{self.pk} {self.full_name} - {self.car}"

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
            raise ValidationError("Data e kthimit duhet të jetë pas datës së marrjes.")
        if self._state.adding and self.pickup_date < timezone.localdate():
            raise ValidationError("Data e marrjes nuk mund të jetë në të kaluarën.")
        if self.days > self.MAX_DAYS:
            raise ValidationError(f"Rezervimi nuk mund të jetë më shumë se {self.MAX_DAYS} ditë.")
        if (
            self.car_id
            and self.status in ACTIVE_STATUSES
            and self.overlapping(self.car_id, self.pickup_date, self.return_date, self.pk).exists()
        ):
            raise ValidationError("Kjo makinë është e zënë në datat e zgjedhura.")

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