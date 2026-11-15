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


class CancelarRegresionAC32Tests(TestCase):
    """AC32 (parte que se comprueba en C4): cancelar por el endpoint con un clic libera la franja.

    La reserva cancelada deja de ocupar la franja también para quien la canceló: Ana vuelve a
    reservar el mismo horario y queda una sola confirmada. El límite semanal (R13, BR15) es de C3,
    que aún no está en esta rama; el cupo de dos confirmadas y el rechazo de la tercera quedan
    para después de que #24 se una a main.
    """

    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1")
        self.client.force_login(self.ana)
        self.url_reservar = f"/canchas/{self.cancha.pk}/reservas/"

    def test_ac32_tras_cancelar_por_el_endpoint_ana_vuelve_a_reservar_la_misma_franja(self):
        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            alta = self.client.post(self.url_reservar, {"fecha": "2026-11-17", "hora": "18:00"})
        self.assertEqual(alta.status_code, 303)
        primera = models.Reserva.objects.get(usuario=self.ana, estado="confirmada")

        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            cancelacion = self.client.post(f"/reservas/{primera.pk}/cancelar/")
        self.assertEqual(cancelacion.status_code, 303)

        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            nueva = self.client.post(self.url_reservar, {"fecha": "2026-11-17", "hora": "18:00"})
        self.assertEqual(nueva.status_code, 303)

        primera.refresh_from_db()
        self.assertEqual(primera.estado, "cancelada")
        confirmadas = models.Reserva.objects.filter(
            cancha=self.cancha, usuario=self.ana, inicio=INICIO, estado="confirmada"
        )
        self.assertEqual(confirmadas.count(), 1)
        self.assertNotEqual(confirmadas.get().pk, primera.pk)
        self.assertEqual(models.Reserva.objects.filter(usuario=self.ana).count(), 2)


class CancelarCanchaDesactivadaTests(TestCase):
    """Revisión de Iván en #23: cancelar en una cancha ya desactivada debe mostrar la confirmación.

    La redirección a la disponibilidad de una cancha inactiva responde 404, así que el jugador
    no vería la confirmación. En ese caso se vuelve al catálogo, donde sí se muestra el aviso.
    """

    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 2", deporte="Fútbol 5", activa=False)
        self.ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1")
        self.reserva = models.Reserva.objects.create(cancha=self.cancha, usuario=self.ana, inicio=INICIO)
        self.client.force_login(self.ana)

    def test_ac11_cancelar_en_cancha_desactivada_vuelve_al_catalogo_con_la_confirmacion(self):
        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            respuesta = self.client.post(f"/reservas/{self.reserva.pk}/cancelar/")

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(respuesta["Location"], "/canchas/")
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "cancelada")

        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            siguiente = self.client.get(respuesta["Location"])
        self.assertEqual(siguiente.status_code, 200)
        self.assertContains(siguiente, "Reserva cancelada")
