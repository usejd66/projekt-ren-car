from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("cars/", views.cars, name="cars"),
    path("explore-fleet/", views.explore_fleet, name="explorefleet"),
    path("contact/", views.contact, name="contact"),
    path("reservation/", views.reservation, name="reservation"),
    path("api/cars/<int:car_id>/availability/", views.car_availability, name="car_availability"),
    path("signup/", views.signup, name="signup"),
    path("subscribe/", views.subscribe, name="subscribe"),

    # Login / logout me sistemin e gatshëm të Django
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
]

