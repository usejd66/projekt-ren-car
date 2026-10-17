import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Car, ContactMessage, Reservation, Subscriber

User = get_user_model()
LOCATIONS = ("Tirana", "Durrës", "Tirana Airport")


class BootstrapFormMixin:
    """Shton klasat e Bootstrap-it automatikisht; `size = "lg"` i bën fushat më të mëdha."""

    size = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", f"{base} {base}-{self.size}" if self.size else base)


class ReservationForm(BootstrapFormMixin, forms.ModelForm):
    size = "lg"
    pickup_location = forms.ChoiceField(
        label="Vendi i marrjes",
        choices=[("", "Select pickup location"), *[(loc, loc) for loc in LOCATIONS]],
    )

    class Meta:
        model = Reservation
        fields = ["car", "full_name", "email", "phone", "pickup_date", "return_date", "pickup_location", "notes"]
        labels = {
            "car": "Makina", "full_name": "Emri i plotë", "email": "Email", "phone": "Telefoni",
            "pickup_date": "Data e marrjes", "return_date": "Data e kthimit", "notes": "Shënime",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "First and last name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+355 ...", "autocomplete": "tel"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["car"].queryset = Car.objects.filter(is_available=True)

    def clean_full_name(self):
        name = " ".join(self.cleaned_data["full_name"].split())
        if len(name) < 3 or re.search(r"\d", name):
            raise forms.ValidationError("Shkruani emrin dhe mbiemrin.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"\+?[\d\s()-]+", phone) or not 7 <= len(re.sub(r"\D", "", phone)) <= 15:
            raise forms.ValidationError("Shkruani një numër telefoni të vlefshëm.")
        return phone


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
        labels = {"name": "Emri", "email": "Email", "subject": "Subjekti", "message": "Mesazhi"}


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ky email është përdorur tashmë.")
        return email


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        error_messages = {"email": {"unique": "Ky email është abonuar tashmë."}}