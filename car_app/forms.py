import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .branding import LOCATIONS
from .models import Car, ContactMessage, Reservation, Subscriber

User = get_user_model()


class BootstrapFormMixin:
    """Shton klasat e Bootstrap-it automatikisht; `size = "lg"` i bën fushat më të mëdha."""

    size = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", f"{base} {base}-{self.size}" if self.size else base)

    def full_clean(self):
        super().full_clean()
        # fushat me gabim marrin kuadrin e kuq të Bootstrap-it
        for name in self.errors:
            if name in self.fields:
                widget = self.fields[name].widget
                widget.attrs["class"] = widget.attrs.get("class", "") + " is-invalid"


class ReservationForm(BootstrapFormMixin, forms.ModelForm):
    pickup_location = forms.ChoiceField(
        label="Pickup location",
        choices=[("", "Select a location"), *[(loc, loc) for loc in LOCATIONS]],
    )

    class Meta:
        model = Reservation
        fields = ["car", "full_name", "email", "phone", "pickup_date", "return_date", "pickup_location", "notes"]
        labels = {
            "car": "Car", "full_name": "Full name", "email": "Email", "phone": "Phone",
            "pickup_date": "Pickup date", "return_date": "Return date", "notes": "Notes",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "First and last name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+355 ...", "autocomplete": "tel"}),
            "pickup_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "return_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["car"].queryset = Car.objects.filter(is_available=True)

    def clean_full_name(self):
        name = " ".join(self.cleaned_data["full_name"].split())
        if len(name) < 3 or re.search(r"\d", name):
            raise forms.ValidationError("Please enter your first and last name.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"\+?[\d\s()-]+", phone) or not 7 <= len(re.sub(r"\D", "", phone)) <= 15:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone

    def clean(self):
        data = super().clean()
        pickup, back = data.get("pickup_date"), data.get("return_date")
        if pickup and pickup < timezone.localdate():
            self.add_error("pickup_date", "The pickup date cannot be in the past.")
        if pickup and back and back <= pickup:
            self.add_error("return_date", "The return date must be after the pickup date.")
        return data


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
        labels = {"name": "Name", "email": "Email", "subject": "Subject", "message": "Message"}


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        error_messages = {"email": {"unique": "This email is already subscribed."}}