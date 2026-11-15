from django.conf import settings
from django.db import models
from django.db.models import Q


class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    deporte = models.CharField(max_length=60)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        constraints = [
            models.CheckConstraint(condition=~Q(nombre=""), name="cancha_nombre_no_vacio"),
            models.CheckConstraint(condition=~Q(deporte=""), name="cancha_deporte_no_vacio"),
        ]

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    ESTADOS = [(CONFIRMADA, "Confirmada"), (CANCELADA, "Cancelada")]

    cancha = models.ForeignKey(Cancha, on_delete=models.PROTECT, related_name="reservas")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservas")
    inicio = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default=CONFIRMADA)
    creada_en = models.DateTimeField(auto_now_add=True)
    cancelada_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cancha", "inicio"],
                condition=Q(estado="confirmada"),
                name="reserva_confirmada_unica",
            ),
            models.CheckConstraint(
                condition=Q(estado__in=["confirmada", "cancelada"]),
                name="reserva_estado_valido",
            ),
            models.CheckConstraint(
                condition=(Q(estado="confirmada", cancelada_en__isnull=True) | Q(estado="cancelada", cancelada_en__isnull=False)),
                name="reserva_cancelacion_coherente",
            ),
        ]

    def __str__(self):
        return f"{self.cancha} {self.inicio:%Y-%m-%d %H:%M} ({self.estado})"
