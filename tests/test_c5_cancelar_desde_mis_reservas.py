"""Cancelar desde "Mis reservas" (AC27 en esa pantalla). HU-05 parte 2, R06 y R09.

Reloj fijo: 2026-11-16 10:00 en Panamá. La pantalla reutiliza el endpoint de C4 (D-017); aquí se prueba
que el botón se ofrezca solo donde corresponde (BR14) y que el formulario funcione con el token CSRF real.
Las reservas se preparan directo en la base de datos.
"""
import re
from datetime import datetime
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from src.reservas.models import Cancha, Reserva

PANAMA = ZoneInfo("America/Panama")
AHORA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)
Usuario = get_user_model()
URL = "/mis-reservas/"


def inicio(dia, hora):
    return datetime(2026, 11, dia, hora, tzinfo=PANAMA)


def accion(reserva):
    return f"/reservas/{reserva.pk}/cancelar/"


class CancelarDesdeMisReservasTests(TestCase):
    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1", first_name="Ana")
        self.luis = Usuario.objects.create_user("luis@ejemplo.com", password="clave-segura-2", first_name="Luis")
        reloj = mock.patch("src.reservas.reloj.ahora", return_value=AHORA)
        reloj.start()
        self.addCleanup(reloj.stop)

    def crear(self, usuario, cuando, estado=Reserva.CONFIRMADA):
        cancelada_en = AHORA if estado == Reserva.CANCELADA else None
        return Reserva.objects.create(
            cancha=self.cancha, usuario=usuario, inicio=cuando, estado=estado, cancelada_en=cancelada_en
        )

    def test_ac27_el_boton_aparece_solo_en_confirmadas_propias_dentro_del_plazo(self):
        con_plazo = self.crear(self.ana, inicio(16, 18))
        justo_dos_horas = self.crear(self.ana, inicio(16, 12))
        fuera_de_plazo = self.crear(self.ana, inicio(16, 11))
        ya_cancelada = self.crear(self.ana, inicio(17, 18), Reserva.CANCELADA)
        ya_pasada = self.crear(self.ana, inicio(15, 18))
        ajena = self.crear(self.luis, inicio(17, 9))
        self.client.force_login(self.ana)

        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, accion(con_plazo))
        self.assertContains(respuesta, accion(justo_dos_horas))
        for reserva in (fuera_de_plazo, ya_cancelada, ya_pasada, ajena):
            self.assertNotContains(respuesta, accion(reserva))

    def test_ac27_luis_recibe_el_boton_de_la_suya_y_no_el_de_la_de_ana(self):
        de_ana = self.crear(self.ana, inicio(17, 18))
        de_luis = self.crear(self.luis, inicio(18, 18))
        self.client.force_login(self.luis)

        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, accion(de_luis))
        self.assertNotContains(respuesta, accion(de_ana))

    def test_ac27_cancelar_desde_el_formulario_libera_la_franja_y_quita_el_boton(self):
        reserva = self.crear(self.ana, inicio(17, 18))
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.ana)

        sin_token = cliente.post(accion(reserva))
        self.assertEqual(sin_token.status_code, 403)
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)

        pagina = cliente.get(URL)
        self.assertContains(pagina, accion(reserva))  # el botón sale de esta pantalla
        # El token debe venir dentro del formulario de cancelar, no de otro formulario de la página.
        formulario = re.search(
            rf'<form[^>]*action="{re.escape(accion(reserva))}"[^>]*>(.*?)</form>', pagina.content.decode(), re.S
        )
        token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', formulario.group(1)).group(1)
        respuesta = cliente.post(accion(reserva), {"csrfmiddlewaretoken": token})

        self.assertEqual(respuesta.status_code, 303)
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, Reserva.CANCELADA)
        self.assertEqual(reserva.cancelada_en, AHORA)
        self.assertEqual(Reserva.objects.filter(cancha=self.cancha, estado=Reserva.CONFIRMADA).count(), 0)
        despues = cliente.get(URL)
        self.assertContains(despues, "Cancelada")
        self.assertNotContains(despues, accion(reserva))
