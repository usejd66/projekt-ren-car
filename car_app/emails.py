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
from django.utils import translation
from django.utils.translation import gettext as _

from . import branding

logger = logging.getLogger(__name__)


def _send(template, subject, to, context, reply_to=None, lang=None):
    """Dërgon emailin në gjuhën `lang` (klienti: gjuha e rezervimit; pronari: gjuha kryesore e faqes)."""
    with translation.override(lang or settings.LANGUAGE_CODE):
        _render_and_send(template, str(subject() if callable(subject) else subject), to, context, reply_to)


def _render_and_send(template, subject, to, context, reply_to):
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
        _send("booking_received",
              lambda: _("We received your reservation #%(n)s – %(car)s") % {"n": booking.pk, "car": booking.car},
              [booking.email], ctx, reply_to=[settings.BOOKINGS_EMAIL], lang=booking.language)
        admin_url = settings.SITE_URL.rstrip("/") + reverse("admin:car_app_reservation_change", args=[booking.pk])
        _send("booking_new_owner",
              lambda: _("New reservation #%(n)s: %(car)s, %(start)s – %(end)s") % {
                  "n": booking.pk, "car": booking.car,
                  "start": f"{booking.pickup_date:%d/%m}", "end": f"{booking.return_date:%d/%m}"},
              [settings.BOOKINGS_EMAIL], {**ctx, "admin_url": admin_url}, reply_to=[booking.email])
    _later(send)


def booking_status_changed(booking):
    """Pronari e konfirmoi ose e anuloi rezervimin te admin."""
    if booking.status not in ("confirmed", "cancelled"):
        return
    subjects = {
        "confirmed": lambda: _("Your booking #%(n)s is confirmed – %(car)s") % {"n": booking.pk, "car": booking.car},
        "cancelled": lambda: _("Your booking #%(n)s was cancelled") % {"n": booking.pk},
    }
    _later(lambda: _send(f"booking_{booking.status}", subjects[booking.status], [booking.email],
                         {"booking": booking}, reply_to=[settings.BOOKINGS_EMAIL], lang=booking.language))


def contact_message(message):
    """Mesazh i ri nga faqja Contact: te pronari, me "Reply" direkt te dërguesi."""
    _later(lambda: _send("contact_owner", lambda: _("Contact form: %(subject)s") % {"subject": message.subject},
                         [settings.BOOKINGS_EMAIL], {"message": message}, reply_to=[message.email]))


def booking_cancelled_by_customer(booking, requested):
    """Klienti anuloi (requested=False) ose kërkoi anulim (requested=True) nga 'My bookings'."""
    def send():
        admin_url = settings.SITE_URL.rstrip("/") + reverse("admin:car_app_reservation_change", args=[booking.pk])
        subject = (lambda: _("Cancellation request: reservation #%(n)s – %(car)s") % {"n": booking.pk, "car": booking.car}) \
            if requested else \
            (lambda: _("Cancelled by customer: reservation #%(n)s – %(car)s") % {"n": booking.pk, "car": booking.car})
        _send("booking_cancel_owner", subject,
              [settings.BOOKINGS_EMAIL], {"booking": booking, "requested": requested, "admin_url": admin_url},
              reply_to=[booking.email])
        if not requested:
            _send("booking_cancelled", lambda: _("Your booking #%(n)s was cancelled") % {"n": booking.pk},
                  [booking.email], {"booking": booking}, reply_to=[settings.BOOKINGS_EMAIL], lang=booking.language)
    _later(send)
