from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Car, ContactMessage, Reservation, Subscriber

User = get_user_model()


class BootstrapFormMixin:
    """U shton klasat e Bootstrap-it të gjitha fushave automatikisht."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)


class ReservationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "car",
            "full_name",
            "email",
            "phone",
            "pickup_date",
            "return_date",
            "pickup_location",
            "notes",
        ]
        widgets = {
            "pickup_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "return_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "car": "Makina",
            "full_name": "Emri i plotë",
            "email": "Email",
            "phone": "Telefoni",
            "pickup_date": "Data e marrjes",
            "return_date": "Data e kthimit",
            "pickup_location": "Vendi i marrjes",
            "notes": "Shënime (opsionale)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["car"].queryset = Car.objects.filter(is_available=True)
        self.fields["car"].empty_label = "Zgjidh makinën"

        today = timezone.localdate().isoformat()
        self.fields["pickup_date"].widget.attrs["min"] = today
        self.fields["return_date"].widget.attrs["min"] = today


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
        labels = {
            "name": "Emri",
            "email": "Email",
            "subject": "Subjekti",
            "message": "Mesazhi",
        }


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