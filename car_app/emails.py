"""Emailet e faqes: konfirmimi i rezervimit, njoftimet për pronarin, mesazhet nga Contact.

Çdo email ka version tekst + HTML (templates/emails/). Dërgimi bëhet pasi ruhet rezervimi
(transaction.on_commit) dhe një gabim në dërgim nuk e prish kurrë rezervimin: regjistrohet në log.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.urls import reverse

from . import branding

logger = logging.getLogger(__name__)


def _send(template, subject, to, context, reply_to=None):
    context = {"site": branding.site(), "site_url": settings.SITE_URL.rstrip("/"), **context}
    text = render_to_string(f"emails/{template}.txt", context)
    html = render_to_string(f"emails/{template}.html", context)
    message = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, to, reply_to=reply_to)
    message.attach_alternative(html, "text/html")
    try:
        message.send()
    except Exception:  # SMTP i paarritshëm, fjalëkalim i gabuar etj.
        logger.exception("Email '%s' to %s could not be sent", template, to)


def _later(func, *args):
    """Dërgo pasi të ruhet në databazë (nëse transaksioni anulohet, s'dërgohet asgjë)."""
    transaction.on_commit(lambda: func(*args))


def booking_received(booking):
    """Klienti sapo bëri rezervim: email te klienti + njoftim te pronari."""
    def send():
        ctx = {"booking": booking}
        _send("booking_received", f"We received your reservation #{booking.pk} – {booking.car}",
              [booking.email], ctx, reply_to=[settings.BOOKINGS_EMAIL])
        admin_url = settings.SITE_URL.rstrip("/") + reverse("admin:car_app_reservation_change", args=[booking.pk])
        _send("booking_new_owner", f"New reservation #{booking.pk}: {booking.car}, "
              f"{booking.pickup_date:%d/%m} – {booking.return_date:%d/%m}",
              [settings.BOOKINGS_EMAIL], {**ctx, "admin_url": admin_url}, reply_to=[booking.email])
    _later(send)


def booking_status_changed(booking):
    """Pronari e konfirmoi ose e anuloi rezervimin te admin."""
    if booking.status not in ("confirmed", "cancelled"):
        return
    subjects = {
        "confirmed": f"Your booking #{booking.pk} is confirmed – {booking.car}",
        "cancelled": f"Your booking #{booking.pk} was cancelled",
    }
    _later(lambda: _send(f"booking_{booking.status}", subjects[booking.status], [booking.email],
                         {"booking": booking}, reply_to=[settings.BOOKINGS_EMAIL]))


def contact_message(message):
    """Mesazh i ri nga faqja Contact: te pronari, me "Reply" direkt te dërguesi."""
    _later(lambda: _send("contact_owner", f"Contact form: {message.subject}", [settings.BOOKINGS_EMAIL],
                         {"message": message}, reply_to=[message.email]))


def booking_cancelled_by_customer(booking, requested):
    """Klienti anuloi (requested=False) ose kërkoi anulim (requested=True) nga 'My bookings'."""
    def send():
        admin_url = settings.SITE_URL.rstrip("/") + reverse("admin:car_app_reservation_change", args=[booking.pk])
        what = "Cancellation request" if requested else "Cancelled by customer"
        _send("booking_cancel_owner", f"{what}: reservation #{booking.pk} – {booking.car}",
              [settings.BOOKINGS_EMAIL], {"booking": booking, "requested": requested, "admin_url": admin_url},
              reply_to=[booking.email])
        if not requested:
            _send("booking_cancelled", f"Your booking #{booking.pk} was cancelled", [booking.email],
                  {"booking": booking}, reply_to=[settings.BOOKINGS_EMAIL])
    _later(send)
