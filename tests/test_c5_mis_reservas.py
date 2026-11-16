"""Pruebas HTTP de "Mis reservas" (AC15, AC18, AC19, AC26). HU-05, R07 y R08.

El botón de cancelar en esta pantalla (AC27) se prueba en `test_c5_cancelar_desde_mis_reservas.py` (D-017).
Usuarios Ana y Luis; canchas "Cancha 1" y "Cancha 2". Las reservas se preparan directo en la base de datos
para poder tener pasadas, futuras y canceladas sin depender del reloj ni de otros endpoints.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from src.reservas.models import Cancha, Reserva

PANAMA = ZoneInfo("America/Panama")
CANCELADA_EN = datetime(2026, 11, 15, 12, 0, tzinfo=PANAMA)
Usuario = get_user_model()
URL = "/mis-reservas/"


def inicio(dia, hora, mes=11):
    return datetime(2026, mes, dia, hora, tzinfo=PANAMA)


class MisReservasBase(TestCase):
    def setUp(self):
        self.cancha1 = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.cancha2 = Cancha.objects.create(nombre="Cancha 2", deporte="Baloncesto", activa=True)
        self.ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1", first_name="Ana")
        self.luis = Usuario.objects.create_user("luis@ejemplo.com", password="clave-segura-2", first_name="Luis")

    def crear(self, usuario, cancha, cuando, estado=Reserva.CONFIRMADA):
        cancelada_en = CANCELADA_EN if estado == Reserva.CANCELADA else None
        return Reserva.objects.create(
            cancha=cancha, usuario=usuario, inicio=cuando, estado=estado, cancelada_en=cancelada_en
        )

    def ids_mostrados(self, respuesta):
        return [r.pk for r in respuesta.context["reservas"]]


class MisReservasTests(MisReservasBase):
    def test_ac15_ana_ve_solo_las_suyas_pasadas_y_futuras_confirmadas_y_canceladas_la_mas_reciente_primero(self):
        pasada = self.crear(self.ana, self.cancha1, inicio(10, 18))
        futura = self.crear(self.ana, self.cancha1, inicio(20, 18))
        cancelada = self.crear(self.ana, self.cancha2, inicio(18, 18), Reserva.CANCELADA)
        de_luis = self.crear(self.luis, self.cancha1, inicio(19, 19))
        self.client.force_login(self.ana)

        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(self.ids_mostrados(respuesta), [futura.pk, cancelada.pk, pasada.pk])
        self.assertNotIn(de_luis.pk, self.ids_mostrados(respuesta))
        self.assertContains(respuesta, "Confirmada")
        self.assertContains(respuesta, "Cancelada")

    def test_ac15_luis_no_ve_las_reservas_de_ana(self):
        self.crear(self.ana, self.cancha1, inicio(20, 18))
        propia = self.crear(self.luis, self.cancha2, inicio(21, 9))
        self.client.force_login(self.luis)

        respuesta = self.client.get(URL)

        self.assertEqual(self.ids_mostrados(respuesta), [propia.pk])

    def test_ac15_con_el_mismo_inicio_va_primero_la_de_id_mayor(self):
        mismo = inicio(20, 18)
        r1 = self.crear(self.ana, self.cancha1, mismo, Reserva.CANCELADA)
        r2 = self.crear(self.ana, self.cancha1, mismo)
        r3 = self.crear(self.ana, self.cancha2, mismo)
        self.client.force_login(self.ana)

        respuesta = self.client.get(URL)

        self.assertEqual(self.ids_mostrados(respuesta), [r3.pk, r2.pk, r1.pk])

    def test_ac15_muestra_la_cancha_y_la_hora_de_panama_no_la_de_utc(self):
        self.crear(self.ana, self.cancha2, inicio(17, 18))  # 18:00 en Panamá es 23:00 UTC
        self.client.force_login(self.ana)

        respuesta = self.client.get(URL)

        self.assertContains(respuesta, "Cancha 2")
        self.assertContains(respuesta, "18:00")
        self.assertNotContains(respuesta, "23:00")

    def test_ac15_sin_reservas_muestra_un_mensaje_claro(self):
        self.crear(self.ana, self.cancha1, inicio(20, 18))
        self.client.force_login(self.luis)

        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(self.ids_mostrados(respuesta), [])
        self.assertContains(respuesta, "Todavía no tienes reservas")

    def test_ac15_el_historial_conserva_las_reservas_de_una_cancha_que_ya_no_esta_activa(self):
        propia = self.crear(self.ana, self.cancha1, inicio(20, 18))
        self.cancha1.activa = False
        self.cancha1.save()
        self.client.force_login(self.ana)

        respuesta = self.client.get(URL)

        self.assertEqual(self.ids_mostrados(respuesta), [propia.pk])
        self.assertContains(respuesta, "Cancha 1")

    def test_ac18_ver_mis_reservas_no_cambia_ninguna_reserva(self):
        self.crear(self.ana, self.cancha1, inicio(20, 18))
        self.crear(self.ana, self.cancha1, inicio(18, 18), Reserva.CANCELADA)
        antes = list(Reserva.objects.values_list("pk", "estado", "inicio", "cancelada_en"))
        self.client.force_login(self.ana)

        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(list(Reserva.objects.values_list("pk", "estado", "inicio", "cancelada_en")), antes)

    def test_ac19_la_pagina_no_pide_recursos_externos(self):
        self.crear(self.ana, self.cancha1, inicio(20, 18))
        self.client.force_login(self.ana)

        respuesta = self.client.get(URL)
        html = respuesta.content.decode()

        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)

    def test_el_menu_ofrece_mis_reservas_solo_con_sesion(self):
        anonimo = self.client.get("/canchas/")
        self.client.force_login(self.ana)
        con_sesion = self.client.get("/canchas/")

        self.assertNotContains(anonimo, 'href="/mis-reservas/"')
        self.assertContains(con_sesion, 'href="/mis-reservas/"')

    def test_mis_reservas_solo_admite_lectura_y_un_post_responde_405_aunque_no_traiga_token(self):
        self.client.force_login(self.ana)
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.ana)

        respuesta = cliente.post(URL)

        self.assertEqual(respuesta.status_code, 405)


class MisReservasSinSesionTests(MisReservasBase):
    def test_ac26_sin_sesion_lleva_al_inicio_de_sesion_y_no_muestra_ninguna_reserva(self):
        self.crear(self.ana, self.cancha1, inicio(20, 18))

        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta["Location"], "/cuentas/entrar/?next=/mis-reservas/")
        self.assertNotIn(b"Cancha 1", respuesta.content)

    def test_ac26_despues_de_entrar_se_vuelve_a_mis_reservas(self):
        propia = self.crear(self.ana, self.cancha1, inicio(20, 18))

        respuesta = self.client.post(
            "/cuentas/entrar/",
            {"correo": "ana@ejemplo.com", "contrasena": "clave-segura-1", "next": URL},
        )

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(respuesta["Location"], URL)
        self.assertEqual(self.ids_mostrados(self.client.get(URL)), [propia.pk])
