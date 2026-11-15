# Requisitos

Versión 1.1 (agrega R13; el resto no cambia). Cada requisito apunta a una historia de usuario (HU) y a sus criterios de aceptación en `acceptance-criteria.md`.

## Funcionales
| ID | HU | Requisito |
|---|---|---|
| R01 | HU-01 | El sistema mantiene un catálogo de canchas (nombre, deporte, activa) con datos de ejemplo. |
| R02 | HU-01 | Dada una cancha activa y una fecha válida, el sistema muestra las franjas de una hora entre las 07:00 y las 22:00 (hora de Panamá), cada una como libre u ocupada. Las franjas libres que ya no se pueden reservar se marcan como no reservables. |
| R03 | HU-02 | Un usuario con sesión iniciada reserva una cancha en una fecha y una hora de inicio. Se crea una reserva confirmada con sus datos. |
| R04 | HU-03 | Una cancha no puede tener dos reservas confirmadas en la misma franja, tampoco cuando dos solicitudes llegan a la vez. |
| R05 | HU-02 | Se validan la cancha (existe y está activa), la fecha (formato AAAA-MM-DD y válida), la hora (en punto y dentro del horario), que la franja sea futura y que no pase de 14 días calendario de anticipación, contados en hora de Panamá. |
| R06 | HU-04 | Quien hizo una reserva confirmada puede cancelarla con al menos 2 horas de anticipación. La reserva pasa a cancelada y la franja queda libre. Se ofrece desde "Mis reservas" y desde la disponibilidad de la cancha. |
| R07 | HU-05 | Un usuario con sesión iniciada ve sus propias reservas, pasadas y futuras, con su estado y la más reciente primero. |
| R08 | HU-02 | Un usuario se registra con nombre, correo y contraseña, e inicia sesión. Se validan los datos y se rechazan las credenciales inválidas. Sin sesión no se puede reservar, cancelar ni ver "Mis reservas". |
| R09 | HU-01, HU-02, HU-04, HU-05 | Una interfaz web sencilla permite ver disponibilidad, reservar, cancelar y ver mis reservas, sin depender de Internet. |

## No funcionales
| ID | Requisito |
|---|---|
| R10 | La lógica usa un reloj inyectable y trabaja en UTC. Las pruebas no dependen de la fecha del sistema. |
| R11 | Todo error es claro para el usuario y no deja datos a medias. |
| R12 | Hay pruebas automatizadas y la cobertura de la app se mide con coverage.py (meta de 70%, se anota el número real). |
| R13 | HU-02 | Un usuario puede tener como máximo 2 reservas confirmadas por semana (lunes a domingo, hora de Panamá), según la fecha de la franja. |

## Historias de usuario
- **HU-01** Como jugador quiero ver qué franjas de una cancha están libres en una fecha, para reservar sin preguntarle a nadie.
- **HU-02** Como jugador quiero reservar una franja libre, para asegurar mi cancha.
- **HU-03** Como encargado quiero que el sistema no permita reservar dos veces la misma franja, para evitar cruces.
- **HU-04** Como jugador quiero cancelar mi reserva, para liberar la franja si no puedo ir.
- **HU-05** Como jugador quiero ver mis reservas, para saber qué tengo agendado.

Versión 1.0 revisada: fecha 2026-11-15; aprobador(es) Emily (Product) e Ivan (Dev, reviewer de C0)

Versión 1.1: propuesta del 2026-11-15 (cambio de C3, D-019 a D-022), pendiente de la aprobación de Ivan (Dev, reviewer de C3).
