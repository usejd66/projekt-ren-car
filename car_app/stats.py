"""Statistikat "sa klientë solli faqja" – për admin → Results dhe raportin mujor."""
from datetime import date, timedelta

from django.db.models import Count, Sum
from django.utils import timezone

from .models import Lead, Reservation

CONTACT_KINDS = ("whatsapp", "phone", "email", "contact")


def month_range(day):
    """(e para e muajit, e para e muajit tjetër) për datën e dhënë."""
    start = day.replace(day=1)
    end = (start + timedelta(days=32)).replace(day=1)
    return start, end


def period_stats(start, end):
    """Numrat për periudhën [start, end) – datat janë date, jo datetime."""
    leads = Lead.objects.filter(created_at__date__gte=start, created_at__date__lt=end)
    by_kind = dict(leads.values_list("kind").annotate(n=Count("id")).values_list("kind", "n"))
    bookings = Reservation.objects.filter(created_at__date__gte=start, created_at__date__lt=end)
    active = bookings.exclude(status="cancelled")

    sources = {}
    for source, kind, n in leads.values_list("source", "kind").annotate(n=Count("id")).values_list("source", "kind", "n"):
        row = sources.setdefault(source, {"source": source, "bookings": 0, "contacts": 0})
        row["bookings" if kind == "booking" else "contacts"] += n

    return {
        "start": start,
        "end": end - timedelta(days=1),
        "bookings": active.count(),
        "cancelled": bookings.filter(status="cancelled").count(),
        "revenue": active.aggregate(s=Sum("total_price"))["s"] or 0,
        "whatsapp": by_kind.get("whatsapp", 0),
        "phone": by_kind.get("phone", 0),
        "email": by_kind.get("email", 0),
        "contact": by_kind.get("contact", 0),
        "contacts": sum(by_kind.get(k, 0) for k in CONTACT_KINDS),
        "sources": sorted(sources.values(), key=lambda r: -(r["bookings"] * 3 + r["contacts"])),
        "top_cars": list(
            active.values("car__brand", "car__name").annotate(n=Count("id"), revenue=Sum("total_price")).order_by("-n")[:5]
        ),
    }


def last_months(n=6, today=None):
    """Përmbledhje e shkurtër për n muajt e fundit (më i riu i pari)."""
    today = today or timezone.localdate()
    rows, start = [], today.replace(day=1)
    for _ in range(n):
        s, e = month_range(start)
        st = period_stats(s, e)
        rows.append({"month": s, "bookings": st["bookings"], "revenue": st["revenue"], "contacts": st["contacts"]})
        start = (s - timedelta(days=1)).replace(day=1)
    return rows


def previous_month(today=None):
    today = today or timezone.localdate()
    last = today.replace(day=1) - timedelta(days=1)
    return month_range(last)


def parse_month(value):
    """'2026-11' -> (date(2026,11,1), date(2026,12,1))"""
    year, month = map(int, value.split("-"))
    return month_range(date(year, month, 1))
