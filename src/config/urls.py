"""Project routes."""
from django.urls import path

from src.reservas.views import cancelar, catalogo, disponibilidad, entrar, inicio, registro, reservar, salir

urlpatterns = [
    path("", inicio, name="inicio"),
    path("canchas/", catalogo, name="canchas"),
    path("canchas/<int:cancha_id>/disponibilidad/", disponibilidad, name="disponibilidad"),
    path("canchas/<int:cancha_id>/reservas/", reservar, name="reservar"),
    path("reservas/<int:reserva_id>/cancelar/", cancelar, name="cancelar"),
    path("cuentas/registro/", registro, name="registro"),
    path("cuentas/entrar/", entrar, name="entrar"),
    path("cuentas/salir/", salir, name="salir"),
]
