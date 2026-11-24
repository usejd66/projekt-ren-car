from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import SITEMAPS

# Faqet (me gjuhë): "/" = gjuha kryesore, "/en/..." = anglisht. Shih mysite/urls.py.
page_patterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("cars/", views.cars, name="cars"),
    path("cars/<int:pk>/<slug:slug>/", views.car_detail, name="car_detail"),
    path("explore-fleet/", views.explore_fleet, name="explorefleet"),
    path("contact/", views.contact, name="contact"),
    path("rental-terms/", views.rental_terms, name="rental_terms"),
    path("rent-a-car/<slug:slug>/", views.location_page, name="location"),
    path("reservation/", views.reservation, name="reservation"),
    path("reservation/success/", views.reservation_success, name="reservation_success"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("account/bookings/", views.my_bookings, name="my_bookings"),
    path("account/bookings/<int:pk>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("offline/", views.offline, name="offline"),
]

# Pa gjuhë: skedarët teknikë
urlpatterns = [
    path("manifest.webmanifest", views.manifest, name="manifest"),
    path("sw.js", views.service_worker, name="service_worker"),
    path("t/", views.track, name="track"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
]
