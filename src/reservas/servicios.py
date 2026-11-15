"""Casos de uso de la disponibilidad y de las reservas. Las vistas solo orquestan."""
from datetime import datetime, time, timedelta

from django.db import IntegrityError, transaction

from src.reservas import dominio
from src.reservas.models import Reserva


class CanchaInactiva(Exception):
    """La cancha existe pero no se puede reservar (BR09, 409)."""


class FranjaOcupada(Exception):
    """Ya hay una reserva confirmada en esa cancha e inicio (BR05, 409 `franja_ocupada`)."""


class ReservaNoEncontrada(Exception):
    """La reserva no existe o es de otra persona (404, sin revelar datos ajenos)."""


class CancelacionInvalida(Exception):
    """La reserva propia ya está cancelada o no cumple el plazo (409, BR08)."""

    def __init__(self, reserva, mensaje):
        super().__init__(mensaje)
        self.reserva = reserva
        self.mensaje = mensaje


def _rango_del_dia(fecha):
    desde = datetime.combine(fecha, time.min, tzinfo=dominio.ZONA_PANAMA)
    return desde, desde + timedelta(days=1)


def inicios_ocupados(cancha, fecha):
    """Puerto de ocupación: inicios de las reservas confirmadas de la cancha en la fecha civil de Panamá."""
    desde, hasta = _rango_del_dia(fecha)
    return frozenset(
        Reserva.objects.filter(
            cancha=cancha, estado=Reserva.CONFIRMADA, inicio__gte=desde, inicio__lt=hasta
        ).values_list("inicio", flat=True)
    )


def reservas_propias_confirmadas(cancha, fecha, usuario):
    """Mapa inicio -> id de las reservas confirmadas del usuario en esa cancha y fecha civil (AC27)."""
    if usuario is None or not usuario.is_authenticated:
        return {}
    desde, hasta = _rango_del_dia(fecha)
    return dict(
        Reserva.objects.filter(
            cancha=cancha, usuario=usuario, estado=Reserva.CONFIRMADA, inicio__gte=desde, inicio__lt=hasta
        ).values_list("inicio", "pk")
    )


def consultar_disponibilidad(cancha, texto_fecha, ahora, usuario=None):
    """Devuelve (fecha, franjas) para una cancha y una fecha escrita por el usuario.

    Lanza `dominio.FechaInvalida` si la fecha no tiene el formato o no existe.
    Con `usuario`, marca la reserva confirmada propia de cada franja y si todavía se puede cancelar.
    """
    fecha = dominio.parsear_fecha(texto_fecha)
    ocupados = inicios_ocupados(cancha, fecha)
    propias = reservas_propias_confirmadas(cancha, fecha, usuario)
    return fecha, dominio.calcular_disponibilidad(fecha, ocupados, ahora, propias)


def cancelar(usuario, reserva_id, ahora):
    """Cancela una reserva confirmada del propio usuario con al menos 2 horas de antelación (BR08).

    Lanza `ReservaNoEncontrada` (404) si no existe o es ajena, y `CancelacionInvalida` (409)
    si ya estaba cancelada o no cumple el plazo. Ante un rechazo no escribe nada (BR12).
    La transacción es corta; en SQLite es `IMMEDIATE`, así que una cancelación concurrente
    espera y luego ve el estado nuevo. El historial se conserva (BR04).
    """
    with transaction.atomic():
        reserva = Reserva.objects.select_related("cancha").filter(pk=reserva_id, usuario=usuario).first()
        if reserva is None:
            raise ReservaNoEncontrada()
        if reserva.estado != Reserva.CONFIRMADA:
            raise CancelacionInvalida(reserva, "Esa reserva ya está cancelada.")
        if not dominio.puede_cancelar(reserva.inicio, ahora):
            raise CancelacionInvalida(reserva, "Solo se puede cancelar con al menos 2 horas de anticipación.")
        cambiadas = Reserva.objects.filter(pk=reserva.pk, estado=Reserva.CONFIRMADA).update(
            estado=Reserva.CANCELADA, cancelada_en=ahora
        )
        if cambiadas != 1:
            raise CancelacionInvalida(reserva, "Esa reserva ya está cancelada.")
    reserva.estado = Reserva.CANCELADA
    reserva.cancelada_en = ahora
    return reserva


def _hay_confirmada(cancha, inicio):
    return Reserva.objects.filter(cancha=cancha, inicio=inicio, estado=Reserva.CONFIRMADA).exists()


def reservar(usuario, cancha, texto_fecha, texto_hora, ahora):
    """Crea una reserva confirmada. Valida primero y escribe después, en una transacción corta.

    Lanza `FechaInvalida` o `ReservaInvalida` (400), `CanchaInactiva` o `FranjaOcupada` (409).
    Si dos solicitudes compiten por la misma franja, el índice único parcial deja pasar solo una.
    """
    fecha = dominio.parsear_fecha(texto_fecha)
    inicio = dominio.inicio_de_reserva(fecha, texto_hora, ahora)
    if not cancha.activa:
        raise CanchaInactiva()
    try:
        with transaction.atomic():
            if _hay_confirmada(cancha, inicio):
                raise FranjaOcupada()
            return Reserva.objects.create(cancha=cancha, usuario=usuario, inicio=inicio)
    except IntegrityError:
        # Solo la colisión de la franja (índice reserva_confirmada_unica) es FranjaOcupada.
        # Se comprueba con la franja ya liberada: cualquier otro error de integridad se propaga.
        if _hay_confirmada(cancha, inicio):
            raise FranjaOcupada() from None
        raise
