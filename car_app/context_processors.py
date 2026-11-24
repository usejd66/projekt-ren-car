"""Branding-u ({{ site.* }}) dhe flamuri PWA, të disponueshëm në çdo template.

Të dhënat e kompanisë (emri, ngjyra, kontaktet, vendet) ndryshohen te car_app/branding.py.
"""
from django.conf import settings

from . import branding


def site(request):
    # pwa: service worker-i regjistrohet vetëm në produksion (në zhvillim do shfaqte skedarë të vjetër)
    return {"site": branding.site(), "pwa": not settings.DEBUG}
