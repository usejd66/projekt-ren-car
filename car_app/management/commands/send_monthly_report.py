"""Raporti mujor "sa klientë solli faqja", me email te BOOKINGS_EMAIL.

    python manage.py send_monthly_report              # muaji i kaluar
    python manage.py send_monthly_report --month 2026-11

Në server vendose të ekzekutohet automatikisht më 1 të çdo muaji (cron):
    0 8 1 * *  cd /rruga/e/projektit && venv/bin/python manage.py send_monthly_report
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.formats import date_format
from django.utils.translation import gettext as _

from car_app import branding, stats


class Command(BaseCommand):
    help = "Dërgon raportin mujor (rezervime, kontakte, burimet) te BOOKINGS_EMAIL."

    def add_arguments(self, parser):
        parser.add_argument("--month", help="YYYY-MM (parazgjedhur: muaji i kaluar)")
        parser.add_argument("--to", help="adresa (parazgjedhur: BOOKINGS_EMAIL)")

    def handle(self, *args, **options):
        start, end = stats.parse_month(options["month"]) if options["month"] else stats.previous_month()
        prev_start, prev_end = stats.previous_month(start)
        ctx = {
            "site": branding.site(),
            "s": stats.period_stats(start, end),
            "prev": stats.period_stats(prev_start, prev_end),
            "results_url": settings.SITE_URL.rstrip("/") + reverse("admin:car_app_lead_changelist"),
        }
        subject = _("%(name)s – monthly report %(month)s: %(n)s bookings") % {
            "name": ctx["site"]["name"], "month": date_format(start, "F Y"), "n": ctx["s"]["bookings"]}
        to = [options["to"] or settings.BOOKINGS_EMAIL]
        msg = EmailMultiAlternatives(subject, render_to_string("emails/monthly_report.txt", ctx),
                                     settings.DEFAULT_FROM_EMAIL, to)
        msg.attach_alternative(render_to_string("emails/monthly_report.html", ctx), "text/html")
        msg.send()
        self.stdout.write(self.style.SUCCESS(f"Raporti për {start:%B %Y} u dërgua te {', '.join(to)}"))
