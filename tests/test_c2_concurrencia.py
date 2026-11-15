"""AC06: dos solicitudes simultáneas para la misma franja libre; solo una se confirma.

Usa TransactionTestCase y dos hilos con su propio cliente y conexión. Una barrera hace
que ambos arranquen casi al mismo tiempo. La base de datos de esta prueba es un archivo
SQLite, no la memoria compartida (ver plan de pruebas de C2).
"""
import threading
from datetime import datetime
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.db import connections
from django.test import Client, TransactionTestCase

from src.reservas import models
from src.reservas.models import Cancha

PANAMA = ZoneInfo("America/Panama")
AHORA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)
Usuario = get_user_model()


class ReservasSimultaneasTests(TransactionTestCase):
    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.usuarios = [
            Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1"),
            Usuario.objects.create_user("luis@ejemplo.com", password="clave-segura-2"),
        ]

    def test_ac06_dos_solicitudes_a_la_vez_dejan_una_sola_confirmada_y_un_conflicto(self):
        barrera = threading.Barrier(2)
        estados = []
        errores = []

        def solicitar(usuario):
            try:
                cliente = Client()
                cliente.force_login(usuario)
                barrera.wait(timeout=10)
                with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
                    respuesta = cliente.post(
                        f"/canchas/{self.cancha.pk}/reservas/", {"fecha": "2026-11-17", "hora": "18:00"}
                    )
                estados.append(respuesta.status_code)
            except Exception as error:  # se informa en el hilo principal
                errores.append(repr(error))
            finally:
                connections.close_all()

        hilos = [threading.Thread(target=solicitar, args=(u,)) for u in self.usuarios]
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join(timeout=30)

        self.assertEqual(errores, [])
        self.assertEqual(sorted(estados), [303, 409])
        self.assertEqual(models.Reserva.objects.filter(estado="confirmada").count(), 1)
