from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def cars(request):
    return render(request, 'cars.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def reservation(request):
    return render(request, 'reservation.html')

def explorefleet(request):
    return render(request, 'explorefleet.html')