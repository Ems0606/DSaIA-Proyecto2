"""Reglas de disponibilidad por fecha civil de Panamá.

Módulo puro: no lee el reloj del sistema ni la base de datos. El instante actual llega
como parámetro. Cubre D-011 y las reglas BR01, BR02, BR06, BR07 y BR13.
"""
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

ZONA_PANAMA = ZoneInfo("America/Panama")
HORA_APERTURA = 7
HORA_CIERRE = 22  # la última franja es 21:00-22:00
HORIZONTE_DIAS = 14
PLAZO_CANCELACION = timedelta(hours=2)  # BR08 y D-011: al menos 2 horas antes del inicio
FORMATO_FECHA = "AAAA-MM-DD"

_PATRON_FECHA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_PATRON_HORA = re.compile(r"[0-9]{2}:[0-9]{2}")


class FechaInvalida(ValueError):
    pass


class ReservaInvalida(ValueError):
    """La hora o la franja pedida no cumple las reglas de reserva (400)."""


@dataclass(frozen=True)
class Franja:
    inicio: datetime
    fin: datetime
    ocupada: bool
    reservable: bool
    propia_id: int | None = None  # id de la reserva confirmada del usuario que consulta (AC27)
    cancelable: bool = False  # propia y con plazo de cancelación (BR08 y BR14)


def parsear_fecha(texto):
    """Convierte 'AAAA-MM-DD' en una fecha civil. Rechaza formatos y fechas imposibles."""
    mensaje = f"La fecha debe escribirse como {FORMATO_FECHA}, por ejemplo 2026-11-17."
    if not _PATRON_FECHA.fullmatch(texto or ""):
        raise FechaInvalida(mensaje)
    try:
        return date.fromisoformat(texto)
    except ValueError:
        raise FechaInvalida(mensaje) from None


def _inicio_local(fecha, hora):
    return datetime(fecha.year, fecha.month, fecha.day, hora, tzinfo=ZONA_PANAMA)


def _es_reservable(inicio, fecha, ahora):
    """BR06 y BR07: la franja empieza después de `ahora` y está dentro de los 14 días de Panamá."""
    hoy = ahora.astimezone(ZONA_PANAMA).date()
    return fecha <= hoy + timedelta(days=HORIZONTE_DIAS) and inicio > ahora


def parsear_hora(texto):
    """Convierte 'HH:MM' en la hora de inicio de una franja (BR01 y BR02)."""
    mensaje = f"La hora debe ser de la forma HH:00 entre {HORA_APERTURA:02d}:00 y {HORA_CIERRE - 1:02d}:00."
    if not _PATRON_HORA.fullmatch(texto or ""):
        raise ReservaInvalida(mensaje)
    hora, minutos = int(texto[:2]), int(texto[3:])
    if minutos != 0 or not HORA_APERTURA <= hora < HORA_CIERRE:
        raise ReservaInvalida(mensaje)
    return hora


def inicio_de_reserva(fecha, texto_hora, ahora):
    """Inicio (hora de Panamá) de la franja pedida, o `ReservaInvalida` si no se puede reservar."""
    inicio = _inicio_local(fecha, parsear_hora(texto_hora))
    if not _es_reservable(inicio, fecha, ahora):
        raise ReservaInvalida(
            "Esa franja ya empezó o está fuera de los 14 días calendario siguientes a hoy."
        )
    return inicio


def puede_cancelar(inicio, ahora):
    """BR08: la reserva se puede cancelar si faltan al menos 2 horas para su inicio (justo 2 horas, sí)."""
    return inicio - ahora >= PLAZO_CANCELACION


def calcular_disponibilidad(fecha, ocupados, ahora, propias=None):
    """Franjas de una hora de la fecha civil, marcadas como ocupadas y reservables.

    `ocupados` es un conjunto de inicios (datetimes con zona) de reservas confirmadas.
    `propias` es un mapa inicio -> id de las reservas confirmadas del usuario que consulta.
    `ahora` es un datetime con zona; la fecha de referencia se toma en Panamá.
    Una franja es reservable si está libre, empieza después de `ahora` (BR06) y su
    fecha no pasa de hoy en Panamá más 14 días calendario, inclusive (BR07).
    """
    propias = propias or {}
    franjas = []
    for hora in range(HORA_APERTURA, HORA_CIERRE):
        inicio = _inicio_local(fecha, hora)
        fin = _inicio_local(fecha, hora + 1)
        ocupada = inicio in ocupados
        reservable = not ocupada and _es_reservable(inicio, fecha, ahora)
        propia_id = propias.get(inicio)
        cancelable = propia_id is not None and puede_cancelar(inicio, ahora)
        franjas.append(
            Franja(
                inicio=inicio,
                fin=fin,
                ocupada=ocupada,
                reservable=reservable,
                propia_id=propia_id,
                cancelable=cancelable,
            )
        )
    return franjas
