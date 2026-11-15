# Reglas de negocio

Versión 1.0 (borrador).

| ID | Regla |
|---|---|
| BR01 | Una reserva dura exactamente una hora y empieza en punto (07:00, 08:00, ... 21:00). |
| BR02 | El horario de funcionamiento es de 07:00 a 22:00 todos los días. La última franja es 21:00 a 22:00. |
| BR03 | Una reserva pertenece a un usuario, una cancha y una franja (fecha y hora de inicio). |
| BR04 | Una reserva tiene estado confirmada o cancelada. Solo las confirmadas bloquean la franja. |
| BR05 | Una cancha solo puede tener una reserva confirmada por franja. Al cancelar, la franja queda libre y otra persona puede reservarla. |
| BR06 | Solo se reserva en el futuro: la franja debe empezar después de la hora actual. |
| BR07 | Se reserva con una anticipación máxima de 14 días calendario: la fecha no puede pasar de hoy más 14 días. |
| BR08 | Solo quien hizo la reserva puede cancelarla, solo si está confirmada y con al menos 2 horas antes del inicio (justo 2 horas todavía se permite). |
| BR09 | Una cancha inactiva no se puede reservar. |
| BR10 | En la v1.0 un usuario puede tener todas las reservas que quiera: no hay límite por usuario. |
| BR11 | El nombre no puede quedar vacío tras recortar espacios, el correo debe tener formato válido y ser único, y la contraseña debe tener al menos 8 caracteres. |
| BR12 | Cuando una operación falla por una regla, no se modifica ningún dato. |

Las decisiones de zona horaria (el horario es hora local de Panamá, UTC-5, y el servidor guarda en UTC) se detallan en `architecture.md`.

Versión 1.0 revisada: fecha ______; aprobador(es) ______
