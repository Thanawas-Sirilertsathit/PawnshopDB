"""URL configuration doing it like interchange to other apps."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("records/", include("records.urls")),
    path("auth/", include("authentication.urls")),
]
