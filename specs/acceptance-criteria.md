# Criterios de aceptación

Versión 1.0 (borrador).

Convención para que sean verificables y repetibles:
- La hora actual de las pruebas es fija: **2026-11-16 10:00** (hora de Panamá), salvo que el criterio diga otra.
- Datos ficticios: usuarios **Ana** y **Luis**, y **Cancha 1** (fútbol 5), que está activa.
- En todo criterio de error, la cantidad de reservas queda igual que antes (BR12).

| ID | Requisito / regla | Criterio |
|---|---|---|
| AC01 | R01, R02, BR01, BR02 | Dada la Cancha 1 sin reservas el 2026-11-17, al consultar la disponibilidad se ven 15 franjas (07:00-08:00 hasta 21:00-22:00), todas libres. |
| AC02 | R02, BR04 | Dada una reserva confirmada de Ana el 2026-11-17 a las 18:00 en la Cancha 1, al consultar ese día la franja de las 18:00 aparece ocupada y las otras 14 libres. |
| AC03 | R02, R05 | Al consultar con una fecha mal escrita ("17/11/2026") o imposible ("2026-02-30"), el sistema responde con un error claro. |
| AC04 | R03, BR03 | Con la sesión de Ana y la franja libre del 2026-11-17 a las 18:00, al reservar se crea una reserva confirmada con la cancha, la fecha, la hora y el usuario, y esa franja pasa a verse ocupada. |
| AC05 | R04, BR05 | Con la reserva de Ana en esa franja, si Luis intenta reservar la misma cancha, fecha y hora, recibe un conflicto y sigue habiendo una sola reserva confirmada. |
| AC06 | R04, BR05 | Si dos solicitudes distintas llegan a la vez para la misma franja libre, solo una queda confirmada y la otra recibe un conflicto. |
| AC07 | R05, BR01, BR02 | Una hora fuera del horario (06:00 o 22:00) o que no empieza en punto (18:30) se rechaza con un error. Los inicios 07:00 y 21:00 sí se aceptan. |
| AC08 | R05, R10, BR06 | Con la hora actual en 2026-11-16 10:00, reservar el mismo día a las 09:00 o a las 10:00 se rechaza porque la franja no es futura. A las 11:00 sí se permite. |
| AC09 | R05, R10, BR07 | Con la hora actual en 2026-11-16 10:00, reservar el 2026-11-30 a las 21:00 se permite y reservar el 2026-12-01 a las 07:00 se rechaza. El límite es de 14 días calendario, no de 336 horas. |
| AC10 | R05, BR09 | Reservar una cancha inactiva o que no existe se rechaza con un error. |
| AC11 | R04, R06, BR05, BR08 | Ana cancela su reserva del 2026-11-17 a las 18:00 con la hora actual en 2026-11-16 10:00: queda cancelada, la franja se ve libre y Luis puede reservarla, con lo que vuelve a haber una sola reserva confirmada en esa franja. |
| AC12 | R06, R10, BR08 | Con la hora actual en 2026-11-17 16:30 (menos de 2 horas antes), cancelar se rechaza y la reserva sigue confirmada. Con la hora actual en 2026-11-17 16:00 (justo 2 horas antes), sí se permite. |
| AC13 | R06, BR08 | Si Luis intenta cancelar la reserva de Ana, se rechaza y la reserva sigue confirmada. |
| AC14 | R06, BR08 | Cancelar una reserva que ya está cancelada se rechaza con un error. |
| AC15 | R07, BR03 | "Mis reservas" de Ana muestra solo sus reservas, pasadas y futuras, confirmadas y canceladas, con la más reciente primero (por inicio y, si empatan, la de ID mayor primero). Luis no ve las de Ana. |
| AC16 | R08, BR11 | Registrarse con el nombre vacío o solo espacios, con un correo inválido, con un correo ya usado (aunque cambien las mayúsculas o haya espacios en los extremos: Ana@ejemplo.com y ana@ejemplo.com son el mismo) o con una contraseña de menos de 8 caracteres se rechaza y no se crea el usuario. |
| AC17 | R08 | Intentar reservar o cancelar sin sesión iniciada se rechaza (se pide iniciar sesión) y no se crea ni cambia ninguna reserva. |
| AC18 | R11, BR12 | Después de cualquier rechazo de los criterios anteriores, la cantidad de reservas y su estado son los mismos que antes del intento. |
| AC19 | R09 | En el navegador, sin conexión a Internet, se puede ver la disponibilidad, reservar, cancelar y ver mis reservas. Se comprueba en QA con datos de prueba y se guardan capturas. |
| AC20 | R03, BR10 | En la v1.0 Ana puede tener varias reservas confirmadas a la vez (por ejemplo tres, en franjas distintas de la misma semana) y todas se aceptan, porque no hay límite por usuario. |
| AC21 | R01, R02, BR09 | Consultar la disponibilidad de una cancha que no existe o que está inactiva responde que no existe (404) y no muestra franjas. |
| AC22 | R02, R10, BR06, BR07, BR13 | Con la hora actual en 2026-11-16 10:00, al consultar la Cancha 1 el 2026-11-15 (pasado) o el 2026-12-01 (fuera de plazo) se ven las franjas, pero ninguna ofrece reservar. El 2026-11-16 muestra como no reservables las franjas de 07:00 a 10:00 y como reservables las libres desde las 11:00. |
| AC23 | R05, R10, BR07 | Con la hora actual en 2026-11-16 21:30 en Panamá (en UTC ya es el 2026-11-17), el plazo se cuenta desde el día de Panamá: reservar el 2026-11-30 a las 21:00 se permite y reservar el 2026-12-01 se rechaza. |
| AC24 | R08, BR11 | Un registro válido crea el usuario y permite iniciar sesión con ese correo (sin distinguir mayúsculas) y su contraseña; con la sesión abierta se puede reservar y cancelar. |
| AC25 | R08 | Iniciar sesión con una contraseña incorrecta o con un correo que no existe se rechaza con un mensaje que no revela cuál de los dos falló, y no abre sesión. |
| AC26 | R07, R08 | Entrar a "Mis reservas" sin sesión iniciada lleva al inicio de sesión y no muestra ninguna reserva. |
| AC27 | R06, R09, BR14 | Cancelar se ofrece solo en las reservas confirmadas propias que todavía cumplen el plazo, tanto en "Mis reservas" como en la disponibilidad de la cancha. No aparece en reservas ajenas, ya canceladas o fuera de plazo. |

Versión 1.0 revisada: fecha ______; aprobador(es) ______
