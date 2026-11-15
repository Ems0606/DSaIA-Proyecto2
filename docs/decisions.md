# Decisiones del equipo

Las decisiones humanas, con fecha. No se reescriben; si una queda obsoleta, se anota aparte.

| ID | Fecha | Decisión | Quién la tomó |
|---|---|---|---|
| D-001 | 2026-11-14 | Dominio: reservas de canchas deportivas | Emily |
| D-002 | 2026-11-14 | Stack igual al del Proyecto 1: Python 3.12, Django 5.2, SQLite, plantillas de Django | Emily |
| D-003 | 2026-11-14 | Repositorio nuevo, público (`DSaIA-Proyecto2`), código desde cero | Emily |
| D-004 | 2026-11-14 | Un ciclo es una historia de usuario con sus issues relacionadas; comparten los mismos roles y los roles rotan por ciclo | Emily |
| D-005 | 2026-11-14 | Cambio de requerimiento simulado a mitad del avance: máximo 2 reservas activas por usuario por semana | Emily |
| D-006 | 2026-11-14 | Alcance: núcleo (disponibilidad, reservar, no doble reserva, cancelar) más "Mis reservas"; interfaz web sencilla | Emily |
| D-007 | 2026-11-14 | Cobertura mínima propuesta de 70% con coverage.py, y se anota el número real | Emily |
| D-008 | 2026-11-14 | Fecha de entrega: lunes 16 de noviembre de 2026 | Dato dado por Emily |
| D-009 | 2026-11-15 | Propuesta #3: presentar fechas en America/Panama, persistir instantes en UTC y recibir la hora por un reloj inyectable. Los valores de horario, duración, horizonte y cancelación siguen por confirmar. | Ivan, pendiente de revisión por Emily |
| D-010 | 2026-11-15 | Propuesta #3: impedir doble reserva con un índice único parcial sobre cancha e inicio para las confirmadas; usar transacciones cortas en SQLite y verificar el conflicto con dos conexiones. | Ivan, pendiente de revisión por Emily |
