"""Project routes."""
from django.urls import path

from src.reservas.views import catalogo, disponibilidad, inicio

urlpatterns = [
    path("", inicio, name="inicio"),
    path("canchas/", catalogo, name="canchas"),
    path("canchas/<int:cancha_id>/disponibilidad/", disponibilidad, name="disponibilidad"),
]
