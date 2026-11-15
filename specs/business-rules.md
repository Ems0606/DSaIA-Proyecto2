# Reglas de negocio

Versión 1.1 (BR10 queda reemplazada por BR15).

Horario, duración de la franja, plazo máximo y plazo de cancelación confirmados por Emily el 2026-11-15 (D-011 en `docs/decisions.md`).

| ID | Regla |
|---|---|
| BR01 | Una reserva dura exactamente una hora y empieza en punto (07:00, 08:00, ... 21:00). |
| BR02 | El horario de funcionamiento es de 07:00 a 22:00, hora de Panamá, todos los días. La última franja es 21:00 a 22:00. |
| BR03 | Una reserva pertenece a un usuario, una cancha y una franja (fecha y hora de inicio). |
| BR04 | Una reserva tiene estado confirmada o cancelada. Solo las confirmadas bloquean la franja. |
| BR05 | Una cancha solo puede tener una reserva confirmada por franja. Al cancelar, la franja queda libre y otra persona puede reservarla. |
| BR06 | Solo se reserva en el futuro: la franja debe empezar después de la hora actual. |
| BR07 | Se reserva con una anticipación máxima de 14 días calendario, inclusive: la fecha local de Panamá de la franja no puede pasar de la fecha local de hoy más 14 días. Se cuenta por día calendario, no por horas, y con la fecha de Panamá aunque en UTC ya sea otro día. |
| BR08 | Solo quien hizo la reserva puede cancelarla, solo si está confirmada y con al menos 2 horas antes del inicio (justo 2 horas todavía se permite). |
| BR09 | Una cancha inactiva no se puede reservar. |
| BR10 | En la v1.0 un usuario puede tener todas las reservas que quiera: no hay límite por usuario. Reemplazada por BR15 en la v1.1. |
| BR11 | El nombre no puede quedar vacío tras recortar espacios, el correo debe tener formato válido y ser único sin distinguir mayúsculas ni espacios en los extremos (Ana@ejemplo.com y ana@ejemplo.com son el mismo correo), y la contraseña debe tener al menos 8 caracteres. |
| BR12 | Cuando una operación falla por una regla, no se modifica ningún dato. |
| BR13 | La disponibilidad se consulta para cualquier fecha válida de una cancha activa. Las franjas libres que incumplen BR06 o BR07 se muestran como no reservables y no ofrecen reservar. |
| BR14 | Cancelar se ofrece solo al dueño de una reserva confirmada que todavía cumple BR08, en "Mis reservas" y en la disponibilidad de la cancha. |
| BR15 | Una reserva pertenece a la semana de lunes a domingo, en hora de Panamá, de su franja (no a la de cuando se creó). Un usuario no puede tener más de 2 reservas confirmadas en la misma semana. Las canceladas no cuentan. Las reservas ya existentes que superen el límite se conservan y solo se rechazan las nuevas. |

Las decisiones de zona horaria (el horario es hora local de Panamá, UTC-5, y el servidor guarda en UTC) se detallan en `architecture.md`.

Versión 1.0 revisada: fecha 2026-11-15; aprobador(es) Emily (Product) e Ivan (Dev, reviewer de C0)

Versión 1.1: fecha 2026-11-15 (cambio de C3, D-019 a D-022); aprobador(es) Emily (Product) e Ivan (Dev, reviewer de C3).
