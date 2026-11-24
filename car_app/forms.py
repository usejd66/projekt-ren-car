import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
        label=_("Pickup location"),
        choices=[("", _("Select a location")), *[(loc, loc) for loc in LOCATIONS]],
    )

    class Meta:
        model = Reservation
        fields = ["car", "full_name", "email", "phone", "pickup_date", "return_date", "pickup_location", "notes"]
        labels = {
            "car": _("Car"), "full_name": _("Full name"), "email": _("Email"), "phone": _("Phone"),
            "pickup_date": _("Pickup date"), "return_date": _("Return date"), "notes": _("Notes"),
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": _("First and last name"), "autocomplete": "name"}),
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
            raise forms.ValidationError(_("Please enter your first and last name."))
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"\+?[\d\s()-]+", phone) or not 7 <= len(re.sub(r"\D", "", phone)) <= 15:
            raise forms.ValidationError(_("Please enter a valid phone number."))
        return phone

    def clean(self):
        data = super().clean()
        pickup, back = data.get("pickup_date"), data.get("return_date")
        if pickup and pickup < timezone.localdate():
            self.add_error("pickup_date", _("The pickup date cannot be in the past."))
        if pickup and back and back <= pickup:
            self.add_error("return_date", _("The return date must be after the pickup date."))
        return data


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
        labels = {"name": _("Name"), "email": _("Email"), "subject": _("Subject"), "message": _("Message")}


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label=_("Email"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("An account with this email already exists."))
        return email


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        error_messages = {"email": {"unique": _("This email is already subscribed.")}}