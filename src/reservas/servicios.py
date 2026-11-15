"""Casos de uso de la disponibilidad y de las reservas. Las vistas solo orquestan."""
from datetime import datetime, time, timedelta

from django.db import IntegrityError, transaction

from src.reservas import dominio
from src.reservas.models import Reserva


class CanchaInactiva(Exception):
    """La cancha existe pero no se puede reservar (BR09, 409)."""


class FranjaOcupada(Exception):
    """Ya hay una reserva confirmada en esa cancha e inicio (BR05, 409 `franja_ocupada`)."""


class LimiteSemanal(Exception):
    """El usuario ya tiene dos confirmadas en la semana de Panamá (BR15, 409)."""


def inicios_ocupados(cancha, fecha):
    """Puerto de ocupación: inicios de las reservas confirmadas de la cancha en la fecha civil de Panamá."""
    desde = datetime.combine(fecha, time.min, tzinfo=dominio.ZONA_PANAMA)
    hasta = desde + timedelta(days=1)
    return frozenset(
        Reserva.objects.filter(
            cancha=cancha, estado=Reserva.CONFIRMADA, inicio__gte=desde, inicio__lt=hasta
        ).values_list("inicio", flat=True)
    )


def consultar_disponibilidad(cancha, texto_fecha, ahora):
    """Devuelve (fecha, franjas) para una cancha y una fecha escrita por el usuario.

    Lanza `dominio.FechaInvalida` si la fecha no tiene el formato o no existe.
    """
    fecha = dominio.parsear_fecha(texto_fecha)
    ocupados = inicios_ocupados(cancha, fecha)
    return fecha, dominio.calcular_disponibilidad(fecha, ocupados, ahora)


def _hay_confirmada(cancha, inicio):
    return Reserva.objects.filter(cancha=cancha, inicio=inicio, estado=Reserva.CONFIRMADA).exists()


def _alcanzo_limite_semanal(usuario, fecha):
    lunes = fecha - timedelta(days=fecha.weekday())
    inicio_semana = datetime.combine(lunes, time.min, tzinfo=dominio.ZONA_PANAMA)
    fin_semana = inicio_semana + timedelta(days=7)
    confirmadas = Reserva.objects.filter(
        usuario=usuario,
        estado=Reserva.CONFIRMADA,
        inicio__gte=inicio_semana,
        inicio__lt=fin_semana,
    )
    return confirmadas.count() >= 2


def reservar(usuario, cancha, texto_fecha, texto_hora, ahora):
    """Crea una reserva confirmada. Valida primero y escribe después, en una transacción corta.

    Lanza `FechaInvalida` o `ReservaInvalida` (400), o un conflicto de cancha, franja o cupo (409).
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
            # SQLite adquiere el bloqueo al entrar en atomic (IMMEDIATE).
            # Contar y crear aquí evita que dos solicitudes gasten el mismo cupo.
            if _alcanzo_limite_semanal(usuario, fecha):
                raise LimiteSemanal()
            return Reserva.objects.create(cancha=cancha, usuario=usuario, inicio=inicio)
    except IntegrityError:
        # Solo la colisión de la franja (índice reserva_confirmada_unica) es FranjaOcupada.
        # Se comprueba con la franja ya liberada: cualquier otro error de integridad se propaga.
        if _hay_confirmada(cancha, inicio):
            raise FranjaOcupada() from None
        raise
