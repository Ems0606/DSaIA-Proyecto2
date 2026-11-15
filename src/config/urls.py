"""Project routes."""
from django.urls import path

from src.reservas.views import catalogo, disponibilidad, entrar, inicio, mis_reservas, registro, reservar, salir

urlpatterns = [
    path("", inicio, name="inicio"),
    path("canchas/", catalogo, name="canchas"),
    path("canchas/<int:cancha_id>/disponibilidad/", disponibilidad, name="disponibilidad"),
    path("canchas/<int:cancha_id>/reservas/", reservar, name="reservar"),
    path("mis-reservas/", mis_reservas, name="mis_reservas"),
    path("cuentas/registro/", registro, name="registro"),
    path("cuentas/entrar/", entrar, name="entrar"),
    path("cuentas/salir/", salir, name="salir"),
]
