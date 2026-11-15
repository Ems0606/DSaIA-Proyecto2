"""Casos de uso de la disponibilidad. Las vistas solo orquestan."""
from src.reservas import dominio


def inicios_ocupados(cancha, fecha):
    """Puerto de ocupación: inicios de las reservas confirmadas de la cancha en la fecha.

    En C1 todavía no hay reservas persistidas (llegan en C2, #6 y #7), así que no hay
    franjas ocupadas. Las pruebas la sustituyen con datos controlados.
    """
    return frozenset()


def consultar_disponibilidad(cancha, texto_fecha, ahora):
    """Devuelve (fecha, franjas) para una cancha y una fecha escrita por el usuario.

    Lanza `dominio.FechaInvalida` si la fecha no tiene el formato o no existe.
    """
    fecha = dominio.parsear_fecha(texto_fecha)
    ocupados = inicios_ocupados(cancha, fecha)
    return fecha, dominio.calcular_disponibilidad(fecha, ocupados, ahora)
