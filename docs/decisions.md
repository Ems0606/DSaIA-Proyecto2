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
| D-011 | 2026-11-15 | Confirmado: horario de 07:00 a 22:00 hora de Panamá, franjas de una hora con último inicio a las 21:00, reservas hasta hoy más 14 días calendario inclusive y cancelación con al menos 2 horas de anticipación | Emily, en respuesta a la pregunta de Ivan |
| D-012 | 2026-11-15 | Se cancela desde "Mis reservas" y desde la disponibilidad de la cancha, solo en reservas propias confirmadas | Emily |
| D-013 | 2026-11-15 | La disponibilidad de una fecha pasada o fuera de plazo muestra las franjas como no reservables | Emily |
| D-014 | 2026-11-15 | Aceptadas las propuestas de Ivan en la revisión del #13: cancha inexistente o inactiva en la disponibilidad responde 404, el correo no distingue mayúsculas ni espacios en los extremos y "Mis reservas" va de la más reciente a la más antigua | Emily, a propuesta de Ivan |
| D-015 | 2026-11-15 | Cuentas con la opción más simple: el sistema de usuarios de Django tal cual, con el correo normalizado (sin espacios en los extremos y en minúsculas) como nombre de usuario, sin verificación de correo ni recuperación de contraseña. Lo que falta para hacerlo robusto queda en `docs/deuda-tecnica.md` | Emily |
| D-016 | 2026-11-15 | Interfaz con HTML y CSS planos servidos por Django, sin librerías externas ni CDN y sin calendario interactivo. Lo que falta queda en `docs/deuda-tecnica.md` | Emily |
