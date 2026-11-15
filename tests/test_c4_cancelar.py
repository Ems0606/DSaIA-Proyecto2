"""Pruebas HTTP de cancelar (AC11, AC12, AC13, AC14, AC17, AC18 y AC27 en la disponibilidad).

Reloj fijo en `src.reservas.reloj.ahora`. Las reservas de partida se crean con el ORM para
no depender de reservar (C2). Usuarios Ana y Luis; la cancha es "Cancha 1".
La cancelación desde "Mis reservas" (AC27 completo) es de C5 (D-017).
"""
import re
from datetime import date, datetime
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.db import OperationalError
from django.test import Client, TestCase

from src.reservas import models
from src.reservas.models import Cancha

PANAMA = ZoneInfo("America/Panama")
AHORA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)
Usuario = get_user_model()


def inicio_panama(texto_fecha, hora):
    f = date.fromisoformat(texto_fecha)
    return datetime(f.year, f.month, f.day, hora, tzinfo=PANAMA)


class CancelarBase(TestCase):
    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1", first_name="Ana")
        self.luis = Usuario.objects.create_user("luis@ejemplo.com", password="clave-segura-2", first_name="Luis")
        self.reserva = self.crear_reserva(self.ana, "2026-11-17", 18)
        self.client.force_login(self.ana)

    def crear_reserva(self, usuario, texto_fecha, hora):
        return models.Reserva.objects.create(
            cancha=self.cancha, usuario=usuario, inicio=inicio_panama(texto_fecha, hora)
        )

    def url_cancelar(self, reserva_id=None):
        return f"/reservas/{reserva_id or self.reserva.pk}/cancelar/"

    def cancelar(self, ahora=AHORA, reserva_id=None, cliente=None):
        cliente = cliente if cliente is not None else self.client
        with mock.patch("src.reservas.reloj.ahora", return_value=ahora):
            return cliente.post(self.url_cancelar(reserva_id))

    def consultar(self, ahora=AHORA, cliente=None, fecha="2026-11-17"):
        cliente = cliente if cliente is not None else self.client
        with mock.patch("src.reservas.reloj.ahora", return_value=ahora):
            return cliente.get(f"/canchas/{self.cancha.pk}/disponibilidad/", {"fecha": fecha})

    def estado_de_reservas(self):
        return list(
            models.Reserva.objects.order_by("pk").values_list("pk", "usuario_id", "estado", "inicio", "cancelada_en")
        )


class CancelarAC11Tests(CancelarBase):
    def test_ac11_cancelar_deja_la_reserva_cancelada_y_redirige_con_confirmacion(self):
        respuesta = self.cancelar()

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(respuesta["Location"], f"/canchas/{self.cancha.pk}/disponibilidad/?fecha=2026-11-17")
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertEqual(self.reserva.cancelada_en, AHORA)

    def test_ac11_la_confirmacion_de_cancelacion_se_muestra_en_la_disponibilidad(self):
        self.cancelar()

        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            respuesta = self.client.get(f"/canchas/{self.cancha.pk}/disponibilidad/", {"fecha": "2026-11-17"})

        self.assertContains(respuesta, "Reserva cancelada")

    def test_ac11_la_franja_queda_libre_y_luis_puede_reservarla_sin_duplicar(self):
        self.cancelar()

        franja = next(f for f in self.consultar().context["franjas"] if f.inicio.hour == 18)
        self.assertFalse(franja.ocupada)

        self.client.force_login(self.luis)
        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            respuesta = self.client.post(
                f"/canchas/{self.cancha.pk}/reservas/", {"fecha": "2026-11-17", "hora": "18:00"}
            )

        self.assertEqual(respuesta.status_code, 303)
        confirmadas = models.Reserva.objects.filter(
            cancha=self.cancha, inicio=inicio_panama("2026-11-17", 18), estado="confirmada"
        )
        self.assertEqual(confirmadas.count(), 1)
        self.assertEqual(confirmadas.get().usuario, self.luis)
        # BR04: la reserva de Ana sigue en la base con su estado cancelada.
        self.assertTrue(models.Reserva.objects.filter(pk=self.reserva.pk, estado="cancelada").exists())


class CancelarAC12Tests(CancelarBase):
    def test_ac12_a_las_16_30_con_reserva_a_las_18_se_rechaza_y_sigue_confirmada(self):
        ahora = datetime(2026, 11, 17, 16, 30, tzinfo=PANAMA)

        respuesta = self.cancelar(ahora=ahora)

        self.assertEqual(respuesta.status_code, 409)
        self.assertContains(respuesta, "2 horas", status_code=409)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "confirmada")
        self.assertIsNone(self.reserva.cancelada_en)

    def test_ac12_justo_a_las_16_00_con_reserva_a_las_18_todavia_se_permite(self):
        ahora = datetime(2026, 11, 17, 16, 0, tzinfo=PANAMA)

        respuesta = self.cancelar(ahora=ahora)

        self.assertEqual(respuesta.status_code, 303)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertEqual(self.reserva.cancelada_en, ahora)

    def test_ac12_una_reserva_que_ya_empezo_no_se_puede_cancelar(self):
        ahora = datetime(2026, 11, 17, 18, 30, tzinfo=PANAMA)

        respuesta = self.cancelar(ahora=ahora)

        self.assertEqual(respuesta.status_code, 409)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "confirmada")


class CancelarAC13Tests(CancelarBase):
    def test_ac13_luis_no_puede_cancelar_la_reserva_de_ana_y_no_se_revelan_datos(self):
        self.client.force_login(self.luis)
        antes = self.estado_de_reservas()

        respuesta = self.cancelar()

        self.assertEqual(respuesta.status_code, 404)
        self.assertNotContains(respuesta, "ana@ejemplo.com", status_code=404)
        self.assertNotContains(respuesta, "18:00", status_code=404)
        self.assertEqual(self.estado_de_reservas(), antes)

    def test_ac13_una_reserva_inexistente_responde_404_y_no_cambia_nada(self):
        antes = self.estado_de_reservas()

        respuesta = self.cancelar(reserva_id=999999)

        self.assertEqual(respuesta.status_code, 404)
        self.assertEqual(self.estado_de_reservas(), antes)


class CancelarAC14Tests(CancelarBase):
    def test_ac14_cancelar_una_reserva_ya_cancelada_se_rechaza_con_mensaje_claro(self):
        self.assertEqual(self.cancelar().status_code, 303)
        self.reserva.refresh_from_db()
        marca_primera = self.reserva.cancelada_en

        respuesta = self.cancelar(ahora=datetime(2026, 11, 16, 11, 0, tzinfo=PANAMA))

        self.assertEqual(respuesta.status_code, 409)
        self.assertContains(respuesta, "ya está cancelada", status_code=409)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertEqual(self.reserva.cancelada_en, marca_primera)


class CancelarAC17Tests(CancelarBase):
    def test_ac17_sin_sesion_se_redirige_al_acceso_y_no_cambia_nada(self):
        antes = self.estado_de_reservas()

        respuesta = self.cancelar(cliente=Client())

        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta["Location"].startswith("/cuentas/entrar/"))
        self.assertEqual(self.estado_de_reservas(), antes)


class CancelarAC18Tests(CancelarBase):
    def test_ac18_los_rechazos_no_cambian_ninguna_reserva(self):
        self.crear_reserva(self.luis, "2026-11-18", 9)
        antes = self.estado_de_reservas()

        self.cancelar(ahora=datetime(2026, 11, 17, 16, 30, tzinfo=PANAMA))  # fuera de plazo
        self.cancelar(reserva_id=999999)  # inexistente
        self.client.force_login(self.luis)
        self.cancelar()  # ajena
        self.cancelar(reserva_id=self.reserva.pk, ahora=datetime(2026, 11, 17, 18, 30, tzinfo=PANAMA))

        self.assertEqual(self.estado_de_reservas(), antes)

    def test_cancelar_solo_admite_post(self):
        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            respuesta = self.client.get(self.url_cancelar())

        self.assertEqual(respuesta.status_code, 405)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "confirmada")


class CancelarBloqueoSqliteTests(CancelarBase):
    def test_503_si_sqlite_agota_la_espera_al_cancelar_y_no_cambia_nada(self):
        antes = self.estado_de_reservas()

        with mock.patch("src.reservas.servicios.cancelar", side_effect=OperationalError("database is locked"), create=True):
            respuesta = self.cancelar()

        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(self.estado_de_reservas(), antes)


class CancelarCsrfTests(CancelarBase):
    def test_post_sin_token_csrf_responde_403_y_no_cambia_nada(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.ana)
        antes = self.estado_de_reservas()

        respuesta = self.cancelar(cliente=cliente)

        self.assertEqual(respuesta.status_code, 403)
        self.assertEqual(self.estado_de_reservas(), antes)

    def test_post_con_el_token_de_la_disponibilidad_cancela(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.ana)
        pagina = self.consultar(cliente=cliente)
        token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', pagina.content.decode())
        self.assertIsNotNone(token, "La disponibilidad debe incluir el token CSRF del botón Cancelar")

        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            respuesta = cliente.post(self.url_cancelar(), {"csrfmiddlewaretoken": token.group(1)})

        self.assertEqual(respuesta.status_code, 303)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, "cancelada")


class CancelarEnDisponibilidadAC27Tests(CancelarBase):
    def test_ac27_ana_ve_cancelar_en_su_reserva_confirmada_dentro_del_plazo(self):
        respuesta = self.consultar()

        self.assertContains(respuesta, f'action="{self.url_cancelar()}"', count=1)

    def test_ac27_luis_ve_la_franja_ocupada_pero_no_ofrece_cancelar(self):
        self.client.force_login(self.luis)

        respuesta = self.consultar()

        self.assertContains(respuesta, 'class="franja ocupada"', count=1)
        self.assertNotContains(respuesta, f'action="{self.url_cancelar()}"')

    def test_ac27_un_visitante_sin_sesion_no_ve_cancelar(self):
        respuesta = self.consultar(cliente=Client())

        self.assertNotContains(respuesta, f'action="{self.url_cancelar()}"')

    def test_ac27_una_reserva_ya_cancelada_no_ofrece_cancelar(self):
        models.Reserva.objects.filter(pk=self.reserva.pk).update(estado="cancelada", cancelada_en=AHORA)

        respuesta = self.consultar()

        self.assertNotContains(respuesta, f'action="{self.url_cancelar()}"')

    def test_ac27_fuera_de_plazo_no_ofrece_cancelar(self):
        respuesta = self.consultar(ahora=datetime(2026, 11, 17, 16, 30, tzinfo=PANAMA))

        self.assertNotContains(respuesta, f'action="{self.url_cancelar()}"')
        self.assertContains(respuesta, 'class="franja ocupada', count=1)
