"""R13, BR15 y AC29–AC35 de la spec v1.1."""
from threading import Barrier, Thread
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import connections
from django.test import Client, TransactionTestCase

from src.reservas.models import Cancha, Reserva
from tests.test_c2_reservar import AHORA, ReservarBase, inicio_panama

Usuario = get_user_model()


class LimiteSemanalTests(ReservarBase):
    def preparar_reserva(self, fecha, hora, *, cancha=None, cancelada=False):
        return Reserva.objects.create(
            cancha=cancha or self.cancha,
            usuario=self.ana,
            inicio=inicio_panama(fecha, hora),
            estado=Reserva.CANCELADA if cancelada else Reserva.CONFIRMADA,
            cancelada_en=AHORA if cancelada else None,
        )

    def estado_reservas(self):
        return list(Reserva.objects.order_by("pk").values())

    def comprobar_limite(self, fecha, hora, **kwargs):
        antes = self.estado_reservas()
        respuesta = self.reservar(fecha, hora, **kwargs)
        self.assertContains(respuesta, "limite_semanal", status_code=409)
        self.assertEqual(self.estado_reservas(), antes)

    def test_r13_ac29_una_confirmada_ya_iniciada_cuenta(self):
        self.preparar_reserva("2026-11-16", 9)
        self.preparar_reserva("2026-11-18", 18)

        self.comprobar_limite("2026-11-20", "18:00")

    def test_r13_ac30_segunda_permitida_y_tercera_rechazada_aunque_cambie_cancha(self):
        otra_cancha = Cancha.objects.create(nombre="Cancha 2", deporte="Tenis")
        self.preparar_reserva("2026-11-17", 18)
        segunda = self.reservar("2026-11-18", "18:00", url=f"/canchas/{otra_cancha.pk}/reservas/")

        self.assertEqual(segunda.status_code, 303)
        self.comprobar_limite("2026-11-20", "18:00")

    def test_r13_ac31_domingo_en_utc_del_lunes_pertenece_a_la_semana_anterior(self):
        self.preparar_reserva("2026-11-16", 18)
        self.preparar_reserva("2026-11-22", 21)

        self.comprobar_limite("2026-11-18", "18:00")
        self.assertEqual(self.reservar("2026-11-23", "07:00").status_code, 303)

    def test_r13_ac32_cancelada_no_ocupa_cupo(self):
        self.preparar_reserva("2026-11-17", 18)
        cancelada = self.preparar_reserva("2026-11-18", 18, cancelada=True)

        self.assertEqual(self.reservar("2026-11-19", "18:00").status_code, 303)
        self.assertEqual(self.confirmadas(), 2)
        self.comprobar_limite("2026-11-20", "18:00")
        cancelada.refresh_from_db()
        self.assertEqual(cancelada.estado, Reserva.CANCELADA)

    def test_r13_ac33_luis_tiene_su_propio_cupo(self):
        self.preparar_reserva("2026-11-17", 18)
        self.preparar_reserva("2026-11-18", 18)
        self.client.force_login(self.luis)

        respuesta = self.reservar("2026-11-20", "18:00")

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(Reserva.objects.filter(usuario=self.luis, estado=Reserva.CONFIRMADA).count(), 1)

    def test_r13_ac34_se_conservan_las_tres_confirmadas_preexistentes(self):
        for dia in ("2026-11-17", "2026-11-18", "2026-11-19"):
            self.preparar_reserva(dia, 18)

        self.comprobar_limite("2026-11-20", "18:00")
        self.assertEqual(self.confirmadas(), 3)

    def test_d022_franja_ocupada_tiene_prioridad_sobre_el_cupo(self):
        self.preparar_reserva("2026-11-17", 18)
        self.preparar_reserva("2026-11-18", 18)
        Reserva.objects.create(
            cancha=self.cancha, usuario=self.luis, inicio=inicio_panama("2026-11-20", 18),
        )
        antes = self.estado_reservas()

        respuesta = self.reservar("2026-11-20", "18:00")

        self.assertContains(respuesta, "franja_ocupada", status_code=409)
        self.assertEqual(self.estado_reservas(), antes)


class LimiteSemanalConcurrenteTests(TransactionTestCase):
    def test_r13_ac35_dos_franjas_distintas_compiten_por_un_cupo(self):
        cancha = Cancha.objects.create(nombre="Cancha 1", deporte="Tenis")
        ana = Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1")
        Reserva.objects.create(cancha=cancha, usuario=ana, inicio=inicio_panama("2026-11-17", 18))
        url = f"/canchas/{cancha.pk}/reservas/"
        clientes = [Client(), Client()]
        for cliente in clientes:
            cliente.force_login(ana)
        barrera = Barrier(2, timeout=10)
        resultados, errores = [], []

        def solicitar(cliente, hora):
            try:
                barrera.wait()
                respuesta = cliente.post(url, {"fecha": "2026-11-20", "hora": hora})
                resultados.append((respuesta.status_code, b"limite_semanal" in respuesta.content))
            except Exception as error:
                errores.append(repr(error))
            finally:
                connections.close_all()

        hilos = [
            Thread(target=solicitar, args=(cliente, hora))
            for cliente, hora in zip(clientes, ("18:00", "19:00"))
        ]
        with patch("src.reservas.reloj.ahora", return_value=AHORA):
            for hilo in hilos:
                hilo.start()
            for hilo in hilos:
                hilo.join(timeout=15)

        self.assertFalse(any(hilo.is_alive() for hilo in hilos))
        self.assertEqual(errores, [])
        self.assertEqual(sorted(resultados), [(303, False), (409, True)])
        confirmadas = Reserva.objects.filter(usuario=ana, estado=Reserva.CONFIRMADA)
        self.assertEqual(confirmadas.count(), 2)
        horas_pedidas = [
            inicio_panama("2026-11-20", hora)
            for hora in (18, 19)
        ]
        self.assertEqual(confirmadas.filter(inicio__in=horas_pedidas).count(), 1)
