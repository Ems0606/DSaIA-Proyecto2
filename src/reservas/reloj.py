"""Reloj de la aplicación: el instante actual en UTC.

Las vistas leen la hora solo a través de `ahora()`, así las pruebas la parchean y no
dependen de la fecha del sistema (R10).
"""
from datetime import datetime, timezone


def ahora():
    return datetime.now(timezone.utc)
