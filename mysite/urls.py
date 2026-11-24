"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from car_app.urls import page_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("car_app.urls")),  # manifest, sw.js, robots.txt, sitemap.xml
]
# faqet në çdo gjuhë: "/" = gjuha kryesore (settings.LANGUAGE_CODE), "/en/..." = anglisht
urlpatterns += i18n_patterns(*page_patterns, prefix_default_language=False)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)