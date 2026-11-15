# Outcomes (ODD)

Versión 1.0 (borrador).

## Problema
Hoy las canchas se reservan por WhatsApp o por llamadas al encargado. Eso produce cruces de horario (dos grupos creen que tienen la misma cancha), obliga a preguntar qué horas están libres y deja al encargado como cuello de botella.

Este planteamiento es un supuesto de partida del equipo. No es un estudio de campo ni hay entrevistas reales.

## Quiénes usan el sistema
- **Jugador o jugadora:** quiere saber qué franjas hay libres y reservar sin esperar respuesta de nadie.
- **Encargado de la cancha:** quiere evitar cruces de horario. En la versión 1.0 no tiene panel propio.

## Outcome
Que ningún horario de una cancha pueda quedar reservado dos veces y que cualquier jugador encuentre franjas libres y reserve sin intervención del encargado.

## Cómo sabremos que se logró
- **O1:** es imposible confirmar dos reservas para la misma cancha y franja, incluso si llegan a la vez. Se comprueba con pruebas automatizadas.
- **O2:** un jugador ve las franjas libres y ocupadas de una cancha en una fecha sin pedir ayuda.
- **O3:** un jugador reserva una franja libre y recibe una confirmación con sus datos.
- **O4:** un jugador puede cancelar y ver sus reservas, y la franja liberada vuelve a estar disponible.

## Preguntas y afirmaciones de exploración
Son supuestos del equipo. Quedan sujetos a confirmación por quien aprueba la spec.

| # | Pregunta o afirmación | Lo que asumimos en la v1.0 | Dónde queda |
|---|---|---|---|
| Q1 | ¿Cuánto dura una reserva? | Una hora exacta | BR01 |
| Q2 | ¿Cuál es el horario de funcionamiento? | De 07:00 a 22:00, todos los días | BR02 |
| Q3 | ¿Con cuánta anticipación se puede reservar? | Hasta 14 días calendario | BR07 |
| Q4 | ¿Quién puede cancelar y hasta cuándo? | Solo quien reservó, con al menos 2 horas de anticipación | BR08 |
| Q5 | ¿Se necesita cuenta? | Sí, usuarios registrados con inicio de sesión | R08 |
| Q6 | ¿Qué pasa si dos personas reservan a la vez? | Solo una se confirma y la otra recibe un conflicto | BR05 |
| Q7 | ¿Hay varias canchas y deportes? | Sí, un catálogo pequeño con datos de ejemplo | R01 |
| Q8 | ¿Hay pagos o notificaciones? | No en la v1.0 | Fuera de alcance |

## Fuera de alcance (v1.0)
Pagos, notificaciones, panel del encargado, reservas recurrentes, varias sedes y multas por cancelación tardía.
