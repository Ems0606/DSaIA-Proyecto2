"""Project routes."""
from django.urls import path

from src.reservas.views import inicio

urlpatterns = [
    path("", inicio, name="inicio"),
]
