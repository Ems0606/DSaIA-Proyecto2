"""Pruebas HTTP de la disponibilidad y del catálogo de canchas (AC01, AC02, AC03, AC21, AC22, AC23).

La hora actual se fija parcheando `src.reservas.reloj.ahora`. La ocupación se inyecta
parcheando `src.reservas.servicios.inicios_ocupados`, porque las reservas persistidas
llegan en C2 (issues #6 y #7).
"""
from datetime import date, datetime, timezone
from io import StringIO
from unittest import mock
from zoneinfo import ZoneInfo

from django.core.management import call_command
from django.test import Client, TestCase

from src.reservas.models import Cancha

PANAMA = ZoneInfo("America/Panama")
AHORA_PRUEBA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)


def inicio_panama(fecha, hora):
    return datetime(fecha.year, fecha.month, fecha.day, hora, tzinfo=PANAMA)


class DisponibilidadVistaTests(TestCase):
    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.url = f"/canchas/{self.cancha.pk}/disponibilidad/"

    def consultar(self, params, ahora=AHORA_PRUEBA):
        with mock.patch("src.reservas.reloj.ahora", return_value=ahora):
            return self.client.get(self.url, params)

    def test_ac01_sin_reservas_se_ven_15_franjas_todas_libres(self):
        respuesta = self.consultar({"fecha": "2026-11-17"})

        self.assertEqual(respuesta.status_code, 200)
        franjas = respuesta.context["franjas"]
        self.assertEqual(len(franjas), 15)
        self.assertFalse(any(f.ocupada for f in franjas))
        self.assertContains(respuesta, "07:00-08:00")
        self.assertContains(respuesta, "21:00-22:00")

    def test_ac02_franja_ocupada_de_las_18_y_las_otras_14_libres(self):
        ocupados = frozenset({inicio_panama(date(2026, 11, 17), 18)})

        with mock.patch("src.reservas.servicios.inicios_ocupados", return_value=ocupados) as fuente:
            respuesta = self.consultar({"fecha": "2026-11-17"})

        self.assertEqual(respuesta.status_code, 200)
        fuente.assert_called_once_with(self.cancha, date(2026, 11, 17))
        franjas = respuesta.context["franjas"]
        self.assertEqual([f.inicio.hour for f in franjas if f.ocupada], [18])
        self.assertEqual(len([f for f in franjas if not f.ocupada]), 14)
        self.assertContains(respuesta, 'class="franja ocupada"', count=1)

    def test_ac03_fecha_con_formato_dd_mm_aaaa_responde_error_sin_franjas(self):
        respuesta = self.consultar({"fecha": "17/11/2026"})

        self.assertEqual(respuesta.status_code, 400)
        self.assertContains(respuesta, "AAAA-MM-DD", status_code=400)
        self.assertFalse(respuesta.context.get("franjas"))
        self.assertNotContains(respuesta, "07:00-08:00", status_code=400)

    def test_ac03_fecha_imposible_responde_error_sin_franjas(self):
        respuesta = self.consultar({"fecha": "2026-02-30"})

        self.assertEqual(respuesta.status_code, 400)
        self.assertContains(respuesta, "AAAA-MM-DD", status_code=400)
        self.assertFalse(respuesta.context.get("franjas"))
        self.assertNotContains(respuesta, "07:00-08:00", status_code=400)

    def test_ac03_fecha_vacia_responde_error_sin_franjas(self):
        respuesta = self.consultar({"fecha": ""})

        self.assertEqual(respuesta.status_code, 400)
        self.assertContains(respuesta, "AAAA-MM-DD", status_code=400)
        self.assertFalse(respuesta.context.get("franjas"))

    def test_ac28_sin_parametro_fecha_muestra_hoy_en_panama_con_200(self):
        # 2026-11-17 02:30 UTC es 2026-11-16 21:30 en Panamá: el día es el 16.
        respuesta = self.consultar({}, ahora=datetime(2026, 11, 17, 2, 30, tzinfo=timezone.utc))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["fecha"], date(2026, 11, 16))
        self.assertEqual(len(respuesta.context["franjas"]), 15)
        self.assertContains(respuesta, 'value="2026-11-16"')

    def test_ac28_head_responde_como_get(self):
        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA_PRUEBA):
            respuesta = self.client.head(self.url)

        self.assertEqual(respuesta.status_code, 200)

    def test_ac28_post_responde_405_aunque_no_traiga_token_csrf(self):
        # Cliente con CSRF activo: el middleware debe ejecutarse antes de la vista.
        cliente = Client(enforce_csrf_checks=True)

        respuesta = cliente.post(self.url)

        self.assertEqual(respuesta.status_code, 405)

    def test_ac21_cancha_inexistente_responde_404_sin_franjas(self):
        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA_PRUEBA):
            respuesta = self.client.get("/canchas/9999/disponibilidad/", {"fecha": "2026-11-17"})

        self.assertEqual(respuesta.status_code, 404)
        self.assertNotContains(respuesta, "07:00-08:00", status_code=404)

    def test_ac21_cancha_inactiva_responde_404_sin_franjas(self):
        cerrada = Cancha.objects.create(nombre="Cancha cerrada", deporte="Fútbol 5", activa=False)

        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA_PRUEBA):
            respuesta = self.client.get(f"/canchas/{cerrada.pk}/disponibilidad/", {"fecha": "2026-11-17"})

        self.assertEqual(respuesta.status_code, 404)
        self.assertNotContains(respuesta, "07:00-08:00", status_code=404)

    def test_ac22_fecha_pasada_se_ve_pero_ninguna_franja_es_reservable(self):
        respuesta = self.consultar({"fecha": "2026-11-15"})

        self.assertEqual(respuesta.status_code, 200)
        franjas = respuesta.context["franjas"]
        self.assertEqual(len(franjas), 15)
        self.assertFalse(any(f.reservable for f in franjas))

    def test_ac22_el_16_a_las_10_las_franjas_hasta_las_10_no_son_reservables_y_desde_las_11_si(self):
        respuesta = self.consultar({"fecha": "2026-11-16"})

        self.assertEqual(respuesta.status_code, 200)
        franjas = respuesta.context["franjas"]
        self.assertEqual([f.inicio.hour for f in franjas if not f.reservable], list(range(7, 11)))
        self.assertEqual([f.inicio.hour for f in franjas if f.reservable], list(range(11, 22)))
        self.assertContains(respuesta, 'class="franja libre no-reservable"', count=4)

    def test_ac22_fecha_fuera_de_plazo_se_ve_pero_ninguna_franja_es_reservable(self):
        respuesta = self.consultar({"fecha": "2026-12-01"})

        self.assertEqual(respuesta.status_code, 200)
        franjas = respuesta.context["franjas"]
        self.assertEqual(len(franjas), 15)
        self.assertFalse(any(f.reservable for f in franjas))

    def test_ac23_el_plazo_se_cuenta_con_el_dia_de_panama(self):
        # 2026-11-16 21:30 en Panamá = 2026-11-17 02:30 UTC.
        ahora_utc = datetime(2026, 11, 17, 2, 30, tzinfo=timezone.utc)

        permitida = self.consultar({"fecha": "2026-11-30"}, ahora=ahora_utc)
        rechazada = self.consultar({"fecha": "2026-12-01"}, ahora=ahora_utc)

        self.assertEqual(permitida.status_code, 200)
        self.assertTrue(next(f for f in permitida.context["franjas"] if f.inicio.hour == 21).reservable)
        self.assertEqual(rechazada.status_code, 200)
        self.assertFalse(any(f.reservable for f in rechazada.context["franjas"]))


class CatalogoCanchasTests(TestCase):
    def test_r01_el_catalogo_muestra_solo_las_canchas_activas(self):
        Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        Cancha.objects.create(nombre="Cancha cerrada", deporte="Fútbol 5", activa=False)

        respuesta = self.client.get("/canchas/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Cancha 1")
        self.assertNotContains(respuesta, "Cancha cerrada")

    def test_r01_la_carga_demo_es_repetible_y_no_duplica_canchas(self):
        salida = StringIO()

        call_command("cargar_demo_canchas", stdout=salida)
        call_command("cargar_demo_canchas", stdout=salida)

        canchas = Cancha.objects.filter(nombre="Cancha 1")
        self.assertEqual(canchas.count(), 1)
        self.assertEqual(canchas.get().deporte, "Fútbol 5")
        self.assertTrue(canchas.get().activa)
