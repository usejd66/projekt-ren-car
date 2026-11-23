"""Të dhënat e kompanisë, të disponueshme në çdo template si {{ site.phone }} etj.

NDRYSHO KËTU numrin, email-in dhe rrjetet sociale kur të kesh të dhënat reale:
përditësohen automatikisht në navbar, footer, Contact, faqen kryesore dhe FAQ.
"""
from .forms import LOCATIONS

SITE = {
    "name": "DriveOn",
    "phone": "+355 69 000 0000",
    "phone_link": "+355690000000",       # pa hapësira, për tel: dhe WhatsApp
    "email": "info@driveon.al",
    "address": "Tirana, Albania",
    "hours": "Every day, 08:00 – 20:00",
    "instagram": "https://www.instagram.com/driveon",
    "facebook": "https://www.facebook.com/driveon",
    "locations": LOCATIONS,
}


def site(request):
    return {"site": SITE}
