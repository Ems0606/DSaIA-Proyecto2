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
