"""Pruebas HTTP de reservar (AC04, AC05, AC07, AC08, AC09, AC10, AC17, AC18, AC23 y AC30).

Reloj fijo: 2026-11-16 10:00 en Panamá (15:00 UTC). La hora actual se parchea en
`src.reservas.reloj.ahora`. Usuarios Ana y Luis; la cancha es "Cancha 1".
"""
from datetime import date, datetime
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.test import TestCase

from src.reservas import models
from src.reservas.models import Cancha

PANAMA = ZoneInfo("America/Panama")
AHORA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)
Usuario = get_user_model()


def inicio_panama(texto_fecha, hora):
    f = date.fromisoformat(texto_fecha)
    return datetime(f.year, f.month, f.day, hora, tzinfo=PANAMA)


class ReservarBase(TestCase):
    def setUp(self):
        self.cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Fútbol 5", activa=True)
        self.ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1", first_name="Ana")
        self.luis = Usuario.objects.create_user("luis@ejemplo.com", password="clave-segura-2", first_name="Luis")
        self.url = f"/canchas/{self.cancha.pk}/reservas/"
        self.client.force_login(self.ana)

    def reservar(self, fecha, hora, ahora=AHORA, url=None, cliente=None):
        with mock.patch("src.reservas.reloj.ahora", return_value=ahora):
            return (cliente or self.client).post(url or self.url, {"fecha": fecha, "hora": hora})

    def confirmadas(self):
        return models.Reserva.objects.filter(estado="confirmada").count()

    def total(self):
        return models.Reserva.objects.count()


class ReservarTests(ReservarBase):
    def test_ac04_reservar_crea_una_reserva_confirmada_y_redirige_a_la_disponibilidad(self):
        respuesta = self.reservar("2026-11-17", "18:00")

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(respuesta["Location"], f"/canchas/{self.cancha.pk}/disponibilidad/?fecha=2026-11-17")
        reserva = models.Reserva.objects.get()
        self.assertEqual(reserva.cancha, self.cancha)
        self.assertEqual(reserva.usuario, self.ana)
        self.assertEqual(reserva.estado, "confirmada")
        self.assertEqual(reserva.inicio, inicio_panama("2026-11-17", 18))

    def test_ac04_la_franja_reservada_se_ve_ocupada(self):
        self.reservar("2026-11-17", "18:00")

        with mock.patch("src.reservas.reloj.ahora", return_value=AHORA):
            respuesta = self.client.get(f"/canchas/{self.cancha.pk}/disponibilidad/", {"fecha": "2026-11-17"})

        franjas = respuesta.context["franjas"]
        self.assertEqual([f.inicio.hour for f in franjas if f.ocupada], [18])
        self.assertEqual(len([f for f in franjas if not f.ocupada]), 14)

    def test_ac05_otro_usuario_en_la_misma_franja_recibe_conflicto(self):
        self.reservar("2026-11-17", "18:00")
        self.client.force_login(self.luis)

        respuesta = self.reservar("2026-11-17", "18:00")

        self.assertEqual(respuesta.status_code, 409)
        self.assertContains(respuesta, "franja_ocupada", status_code=409)
        self.assertEqual(self.confirmadas(), 1)

    def test_ac07_inicios_07_y_21_se_aceptan(self):
        self.assertEqual(self.reservar("2026-11-17", "07:00").status_code, 303)
        self.assertEqual(self.reservar("2026-11-17", "21:00").status_code, 303)
        self.assertEqual(self.confirmadas(), 2)

    def test_ac07_horas_fuera_de_horario_o_no_en_punto_se_rechazan(self):
        for hora in ("06:00", "22:00", "18:30", "7", "ab:cd", ""):
            with self.subTest(hora=hora):
                respuesta = self.reservar("2026-11-17", hora)
                self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(self.total(), 0)

    def test_fecha_con_formato_invalido_se_rechaza(self):
        for fecha in ("17/11/2026", "2026-02-30", "hola", ""):
            with self.subTest(fecha=fecha):
                self.assertEqual(self.reservar(fecha, "18:00").status_code, 400)
        self.assertEqual(self.total(), 0)

    def test_ac08_misma_fecha_a_las_09_y_a_las_10_se_rechaza(self):
        self.assertEqual(self.reservar("2026-11-16", "09:00").status_code, 400)
        self.assertEqual(self.reservar("2026-11-16", "10:00").status_code, 400)
        self.assertEqual(self.total(), 0)

    def test_ac08_misma_fecha_a_las_11_se_permite(self):
        self.assertEqual(self.reservar("2026-11-16", "11:00").status_code, 303)
        self.assertEqual(self.confirmadas(), 1)

    def test_ac09_el_dia_30_a_las_21_se_permite_y_el_1_de_diciembre_se_rechaza(self):
        self.assertEqual(self.reservar("2026-11-30", "21:00").status_code, 303)
        self.assertEqual(self.reservar("2026-12-01", "07:00").status_code, 400)
        self.assertEqual(self.confirmadas(), 1)

    def test_ac23_con_las_21_30_de_panama_el_plazo_se_cuenta_desde_el_dia_de_panama(self):
        ahora = datetime(2026, 11, 16, 21, 30, tzinfo=PANAMA)  # en UTC ya es el 17

        self.assertEqual(self.reservar("2026-11-30", "21:00", ahora=ahora).status_code, 303)
        self.assertEqual(self.reservar("2026-12-01", "07:00", ahora=ahora).status_code, 400)
        self.assertEqual(self.confirmadas(), 1)

    def test_ac10_cancha_inactiva_se_rechaza_con_conflicto(self):
        self.cancha.activa = False
        self.cancha.save()

        respuesta = self.reservar("2026-11-17", "18:00")

        self.assertEqual(respuesta.status_code, 409)
        self.assertEqual(self.total(), 0)

    def test_ac10_cancha_inexistente_responde_404(self):
        respuesta = self.reservar("2026-11-17", "18:00", url="/canchas/999/reservas/")

        self.assertEqual(respuesta.status_code, 404)
        self.assertEqual(self.total(), 0)

    def test_r13_ac30_ana_puede_tener_tres_reservas_en_semanas_distintas(self):
        # AC20 de v1.0 pasa a AC30 en v1.1. Las tres fechas caben en el horizonte de 14 días.
        for fecha, hora in (("2026-11-16", "18:00"), ("2026-11-23", "18:00"), ("2026-11-30", "18:00")):
            self.assertEqual(self.reservar(fecha, hora).status_code, 303)
        self.assertEqual(models.Reserva.objects.filter(usuario=self.ana, estado="confirmada").count(), 3)

    def test_reservar_solo_admite_post(self):
        respuesta = self.client.get(self.url)

        self.assertEqual(respuesta.status_code, 405)

    def test_ac18_un_rechazo_no_cambia_las_reservas_existentes(self):
        self.reservar("2026-11-17", "18:00")
        antes = list(models.Reserva.objects.values_list("pk", "estado", "inicio"))

        self.reservar("2026-11-17", "18:30")
        self.reservar("2026-12-01", "07:00")
        self.client.force_login(self.luis)
        self.reservar("2026-11-17", "18:00")

        self.assertEqual(list(models.Reserva.objects.values_list("pk", "estado", "inicio")), antes)


class ReservarSinSesionTests(ReservarBase):
    def test_ac17_sin_sesion_pide_iniciar_sesion_y_no_crea_reserva(self):
        self.client.logout()

        respuesta = self.reservar("2026-11-17", "18:00")

        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta["Location"].startswith("/cuentas/entrar/"))
        self.assertEqual(self.total(), 0)
