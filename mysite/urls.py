"""URL configuration doing it like interchange to other apps."""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/records/', permanent=True)),
    path('admin/', admin.site.urls),
    path("records/", include("records.urls")),
]
