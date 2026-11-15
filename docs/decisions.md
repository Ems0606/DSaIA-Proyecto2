# Decisiones del equipo

Las decisiones humanas, con fecha. No se reescriben; si una queda obsoleta, se anota aparte.

| ID | Fecha | Decisión | Quién la tomó |
|---|---|---|---|
| D-001 | 2026-11-14 | Dominio: reservas de canchas deportivas | Emily |
| D-002 | 2026-11-14 | Stack igual al del Proyecto 1: Python 3.12, Django 5.2, SQLite, plantillas de Django | Emily |
| D-003 | 2026-11-14 | Repositorio nuevo, público (`DSaIA-Proyecto2`), código desde cero | Emily |
| D-004 | 2026-11-14 | Un ciclo es una historia de usuario con sus issues relacionadas; comparten los mismos roles y los roles rotan por ciclo | Emily |
| D-005 | 2026-11-14 | Habrá un cambio de requerimiento a mitad del avance (C3). Su contenido se define y se registra cuando llegue ese ciclo | Emily |
| D-006 | 2026-11-14 | Alcance: núcleo (disponibilidad, reservar, no doble reserva, cancelar) más "Mis reservas"; interfaz web sencilla | Emily |
| D-007 | 2026-11-14 | Cobertura mínima propuesta de 70% con coverage.py, y se anota el número real | Emily |
| D-008 | 2026-11-14 | Fecha de entrega: lunes 16 de noviembre de 2026 | Dato dado por Emily |
| D-009 | 2026-11-15 | Propuesta #3: presentar fechas en America/Panama, persistir instantes en UTC y recibir la hora por un reloj inyectable. Los valores de horario, duración, horizonte y cancelación siguen por confirmar. | Ivan, pendiente de revisión por Emily |
| D-010 | 2026-11-15 | Propuesta #3: impedir doble reserva con un índice único parcial sobre cancha e inicio para las confirmadas; usar transacciones cortas en SQLite y verificar el conflicto con dos conexiones. | Ivan, pendiente de revisión por Emily |
| D-011 | 2026-11-15 | Confirmado: horario de 07:00 a 22:00 hora de Panamá, franjas de una hora con último inicio a las 21:00, reservas hasta hoy más 14 días calendario inclusive y cancelación con al menos 2 horas de anticipación | Emily, en respuesta a la pregunta de Ivan |
| D-012 | 2026-11-15 | Se cancela desde "Mis reservas" y desde la disponibilidad de la cancha, solo en reservas propias confirmadas | Emily |
| D-013 | 2026-11-15 | La disponibilidad de una fecha pasada o fuera de plazo muestra las franjas como no reservables | Emily |
| D-014 | 2026-11-15 | Aceptadas las propuestas de Ivan en la revisión del #13: cancha inexistente o inactiva en la disponibilidad responde 404, el correo no distingue mayúsculas ni espacios en los extremos y "Mis reservas" va de la más reciente a la más antigua | Emily, a propuesta de Ivan |
| D-015 | 2026-11-15 | Cuentas con la opción más simple: el sistema de usuarios de Django tal cual, con el correo normalizado (sin espacios en los extremos y en minúsculas) como nombre de usuario, sin verificación de correo ni recuperación de contraseña. Un modelo de usuario propio y esas funciones quedan para una versión posterior | Emily |
| D-016 | 2026-11-15 | Interfaz con HTML y CSS planos servidos por Django, sin librerías externas ni CDN y sin calendario interactivo. El calendario interactivo queda para una versión posterior | Emily |
| D-017 | 2026-11-15 | Cancelar se entrega en dos pasos: en C4 desde la disponibilidad de la cancha, con el endpoint de cancelación y sus reglas, y en C5 se agrega el botón en "Mis reservas", que reutiliza ese endpoint. AC27 se cierra completo en C5 | Emily, a partir de la revisión de Rey |

Nota del 2026-11-15 sobre D-005: la fila original describía el contenido del cambio de C3. Se retiró ese detalle para no anticiparlo antes de ese ciclo. El texto original sigue en el historial de `main`, y el cambio completo se registra en C3 con su fecha.
