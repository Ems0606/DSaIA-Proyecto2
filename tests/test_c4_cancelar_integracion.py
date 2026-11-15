"""Pruebas de C4 que faltaban: concurrencia al cancelar (arquitectura, punto 3) y AC24 con cuenta real.

- Concurrencia: dos cancelaciones simultáneas de la misma reserva. Una cancela (303) y la otra
  ve el estado nuevo y falla (409) sin volver a escribir `cancelada_en`. Usa TransactionTestCase
  y un archivo SQLite de prueba, como AC06 en C2.
- AC24: el usuario se registra, inicia sesión y cancela su propia reserva por los formularios reales.
"""
import threading
from datetime import datetime
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.db import connections
from django.test import Client, TestCase, TransactionTestCase

from src.reservas import models
from src.reservas.models import Cancha

PANAMA = ZoneInfo("America/Panama")
AHORA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)
INICIO = datetime(2026, 11, 17, 18, 0, tzinfo=PANAMA)
Usuario = get_user_model()


class CancelarConcurrenciaTests(TransactionTestCase):
    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1")
        self.reserva = models.Reserva.objects.create(cancha=self.cancha, usuario=self.ana, inicio=INICIO)

    def test_ac11_dos_cancelaciones_a_la_vez_una_cancela_y_la_otra_ve_el_estado_nuevo(self):
        barrera = threading.Barrier(2)
        estados = []
        errores = []

        def cancelar():
            try:
                cliente = Client()
                cliente.force_login(self.ana)
                barrera.wait(timeout=10)
                with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
                    respuesta = cliente.post(f"/reservas/{self.reserva.pk}/cancelar/")
                estados.append(respuesta.status_code)
            except Exception as error:  # se informa en el hilo principal
                errores.append(repr(error))
            finally:
                connections.close_all()

        hilos = [threading.Thread(target=cancelar) for _ in range(2)]
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join(timeout=30)

        self.assertEqual(errores, [])
        self.assertEqual(sorted(estados), [303, 409])
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertIsNotNone(self.reserva.cancelada_en)
        self.assertEqual(models.Reserva.objects.filter(pk=self.reserva.pk, estado="cancelada").count(), 1)


class CancelarCuentaTests(TestCase):
    """AC24 (parte de cancelar): registro, acceso y cancelación con la cuenta creada."""

    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)

    def test_ac24_un_usuario_registrado_puede_iniciar_sesion_y_cancelar_su_reserva(self):
        cliente = Client()
        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            alta = cliente.post(
                "/cuentas/registro/",
                {"nombre": "Ana", "correo": "  Ana@Ejemplo.com ", "contrasena": "clave-segura-1"},
            )
            self.assertEqual(alta.status_code, 303)

            acceso = cliente.post(
                "/cuentas/entrar/", {"correo": "ana@ejemplo.com", "contrasena": "clave-segura-1"}
            )
            self.assertEqual(acceso.status_code, 303)

            usuario = Usuario.objects.get(username="ana@ejemplo.com")
            reserva = models.Reserva.objects.create(cancha=self.cancha, usuario=usuario, inicio=INICIO)

            cancelacion = cliente.post(f"/reservas/{reserva.pk}/cancelar/")

        self.assertEqual(cancelacion.status_code, 303)
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, "cancelada")
