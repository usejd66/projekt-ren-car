from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('reservation/', views.reservation, name='reservation'),
    path('explorefleet/', views.explorefleet, name='explorefleet'),
]