"""Traducción de errores de integridad en `servicios.reservar` (R04, AC05, AC06).

Solo la colisión de la franja (índice `reserva_confirmada_unica`) significa `FranjaOcupada`.
Cualquier otro error de integridad es un fallo real y no se disfraza de franja ocupada.
"""
from datetime import datetime
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from src.reservas import servicios
from src.reservas.models import Cancha, Reserva

PANAMA = ZoneInfo("America/Panama")
AHORA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)


class TraduccionDeIntegridadTests(TestCase):
    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.ana = get_user_model().objects.create_user("ana@ejemplo.com", password="clave-segura-1")

    def test_r04_otro_error_de_integridad_no_se_traduce_a_franja_ocupada(self):
        with mock.patch.object(Reserva.objects, "create", side_effect=IntegrityError("otra restriccion")):
            with self.assertRaises(IntegrityError):
                servicios.reservar(self.ana, self.cancha, "2026-11-17", "18:00", AHORA)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_r04_si_otra_solicitud_ocupo_la_franja_se_traduce_a_franja_ocupada(self):
        # La comprobación previa no ve nada; al insertar, otra solicitud ya había confirmado la franja.
        with mock.patch.object(servicios, "_hay_confirmada", side_effect=[False, True]):
            with mock.patch.object(Reserva.objects, "create", side_effect=IntegrityError("colision")):
                with self.assertRaises(servicios.FranjaOcupada):
                    servicios.reservar(self.ana, self.cancha, "2026-11-17", "18:00", AHORA)
