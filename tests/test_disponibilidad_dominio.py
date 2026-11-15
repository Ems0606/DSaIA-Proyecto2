"""Pruebas del dominio de disponibilidad (AC01, AC02, AC03, AC22 y frontera AC23).

El dominio es puro: recibe el instante actual como parámetro y no lee el reloj del sistema.
"""
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase

from src.reservas import dominio

PANAMA = ZoneInfo("America/Panama")
AHORA_PRUEBA = datetime(2026, 11, 16, 10, 0, tzinfo=PANAMA)


def inicio_panama(fecha, hora):
    return datetime(fecha.year, fecha.month, fecha.day, hora, tzinfo=PANAMA)


class FranjasDelDiaTests(SimpleTestCase):
    def test_ac01_hay_15_franjas_de_0700_a_2200_hora_de_panama(self):
        franjas = dominio.calcular_disponibilidad(date(2026, 11, 17), frozenset(), AHORA_PRUEBA)

        self.assertEqual(len(franjas), 15)
        self.assertEqual(franjas[0].inicio, inicio_panama(date(2026, 11, 17), 7))
        self.assertEqual(franjas[-1].inicio, inicio_panama(date(2026, 11, 17), 21))
        self.assertEqual(franjas[-1].fin, inicio_panama(date(2026, 11, 17), 22))

    def test_ac01_cada_franja_dura_una_hora(self):
        franjas = dominio.calcular_disponibilidad(date(2026, 11, 17), frozenset(), AHORA_PRUEBA)

        self.assertTrue(all(f.fin - f.inicio == timedelta(hours=1) for f in franjas))

    def test_ac01_sin_reservas_todas_las_franjas_estan_libres(self):
        franjas = dominio.calcular_disponibilidad(date(2026, 11, 17), frozenset(), AHORA_PRUEBA)

        self.assertFalse(any(f.ocupada for f in franjas))


class OcupacionTests(SimpleTestCase):
    def test_ac02_la_franja_de_las_18_aparece_ocupada_y_las_otras_14_libres(self):
        ocupados = frozenset({inicio_panama(date(2026, 11, 17), 18)})

        franjas = dominio.calcular_disponibilidad(date(2026, 11, 17), ocupados, AHORA_PRUEBA)

        ocupadas = [f.inicio.hour for f in franjas if f.ocupada]
        libres = [f for f in franjas if not f.ocupada]
        self.assertEqual(ocupadas, [18])
        self.assertEqual(len(libres), 14)

    def test_una_franja_ocupada_nunca_es_reservable(self):
        ocupados = frozenset({inicio_panama(date(2026, 11, 17), 11)})

        franjas = dominio.calcular_disponibilidad(date(2026, 11, 17), ocupados, AHORA_PRUEBA)

        ocupada = next(f for f in franjas if f.inicio.hour == 11)
        self.assertTrue(ocupada.ocupada)
        self.assertFalse(ocupada.reservable)


class ReservabilidadTests(SimpleTestCase):
    def test_ac22_el_16_a_las_10_las_franjas_hasta_las_10_no_son_reservables_y_desde_las_11_si(self):
        franjas = dominio.calcular_disponibilidad(date(2026, 11, 16), frozenset(), AHORA_PRUEBA)

        for franja in franjas:
            with self.subTest(inicio=franja.inicio.hour):
                self.assertEqual(franja.reservable, franja.inicio.hour >= 11)

    def test_ac22_fecha_pasada_no_tiene_franjas_reservables(self):
        franjas = dominio.calcular_disponibilidad(date(2026, 11, 15), frozenset(), AHORA_PRUEBA)

        self.assertEqual(len(franjas), 15)
        self.assertFalse(any(f.reservable for f in franjas))

    def test_ac22_fecha_fuera_de_plazo_no_tiene_franjas_reservables(self):
        franjas = dominio.calcular_disponibilidad(date(2026, 12, 1), frozenset(), AHORA_PRUEBA)

        self.assertEqual(len(franjas), 15)
        self.assertFalse(any(f.reservable for f in franjas))

    def test_br07_el_dia_14_es_reservable_inclusive(self):
        franjas = dominio.calcular_disponibilidad(date(2026, 11, 30), frozenset(), AHORA_PRUEBA)

        ultima = next(f for f in franjas if f.inicio.hour == 21)
        self.assertTrue(ultima.reservable)

    def test_ac23_el_plazo_se_cuenta_con_el_dia_de_panama_y_no_con_utc(self):
        # 2026-11-16 21:30 en Panamá equivale a 2026-11-17 02:30 UTC.
        ahora_utc = datetime(2026, 11, 17, 2, 30, tzinfo=timezone.utc)

        ultima_permitida = dominio.calcular_disponibilidad(date(2026, 11, 30), frozenset(), ahora_utc)
        primera_rechazada = dominio.calcular_disponibilidad(date(2026, 12, 1), frozenset(), ahora_utc)

        self.assertTrue(next(f for f in ultima_permitida if f.inicio.hour == 21).reservable)
        self.assertFalse(any(f.reservable for f in primera_rechazada))


class FechaTests(SimpleTestCase):
    def test_ac03_acepta_la_fecha_en_formato_aaaa_mm_dd(self):
        self.assertEqual(dominio.parsear_fecha("2026-11-17"), date(2026, 11, 17))

    def test_ac03_rechaza_la_fecha_escrita_como_dd_mm_aaaa(self):
        with self.assertRaises(dominio.FechaInvalida):
            dominio.parsear_fecha("17/11/2026")

    def test_ac03_rechaza_una_fecha_imposible(self):
        with self.assertRaises(dominio.FechaInvalida):
            dominio.parsear_fecha("2026-02-30")

    def test_ac03_rechaza_vacia_mal_formada_o_sin_ceros(self):
        for texto in ["", "2026-1-5", "hoy", "2026-11-17T10:00"]:
            with self.subTest(texto=texto):
                with self.assertRaises(dominio.FechaInvalida):
                    dominio.parsear_fecha(texto)

    def test_ac03_el_mensaje_de_error_indica_el_formato_esperado(self):
        with self.assertRaises(dominio.FechaInvalida) as contexto:
            dominio.parsear_fecha("17/11/2026")

        self.assertIn("AAAA-MM-DD", str(contexto.exception))
