"""sitemap.xml: faqet që duam të gjejë Google (faqet kryesore, çdo makinë, çdo vend marrjeje)."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.text import slugify

from .branding import LOCATIONS
from .models import Car


class StaticSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return ["index", "cars", "about", "contact", "rental_terms"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "index" else 0.7


class CarSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Car.objects.filter(is_available=True).order_by("pk")

    def lastmod(self, car):
        return car.created_at


class LocationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return [slugify(loc) for loc in LOCATIONS]

    def location(self, slug):
        return reverse("location", args=[slug])


SITEMAPS = {"pages": StaticSitemap, "locations": LocationSitemap, "cars": CarSitemap}
