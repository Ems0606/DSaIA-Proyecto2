# Planificación del Proyecto 2 (C0)

Entrega: **lunes 16 de noviembre de 2026** (la hora límite está por confirmar).

## Roles y ciclos
Un ciclo es una historia de usuario con sus issues relacionadas (bugs, tareas técnicas). Todas comparten los mismos roles, y los roles rotan en cada ciclo.

| Ciclo | Contenido | Product / Spec | Arquitectura / Dev | QA / DevOps |
|---|---|---|---|---|
| C0 | Planificación, ODD, specs v1.0, scaffolding y CI | Emily | Ivan | Rey |
| C1 | HU-01 Ver disponibilidad | Ivan | Rey | Emily |
| C2 | HU-02 Reservar, HU-03 No doble reserva, validaciones y cuentas | Rey | Emily | Ivan |
| C3 | Cambio de requerimiento (spec v1.1) | Emily | Ivan | Rey |
| C4 | HU-04 Cancelar | Ivan | Rey | Emily |
| C5 | HU-05 Mis reservas | Rey | Emily | Ivan |
| C6 | Cierre: README, trazabilidad, cobertura, evidencias y presentación | Emily | Ivan | Rey |

En cada tarea el Dev del ciclo es el responsable, el Product es el Reviewer (revisa contra la spec) y QA hace la verificación. En las tareas de specs el responsable es el Product y su Reviewer es el Dev. Nadie aprueba su propio PR.

## Cronograma (hora de Panamá)
- Sábado 14, noche: C0.
- Domingo 15, mañana y tarde: C1 y C2.
- Domingo 15, noche: C3 y C4.
- Lunes 16: C5 y C6, repetir pruebas y entregar.

Si falta tiempo, lo primero que se recorta es el pulido de la web. HU-05 "Mis reservas" está en el alcance de la v1.0 y no se recorta por defecto: si hiciera falta, Product aprueba primero el cambio y se actualizan la spec, la trazabilidad y este checklist. No se recortan las pruebas de doble reserva, el ciclo del cambio de spec ni la trazabilidad.

## Estrategia de pruebas
- Pruebas con el framework de Django (`python manage.py test`) y cobertura con coverage.py. La meta es 70% sobre el código de la app, sin migraciones, y se anota el número real.
- Pruebas primero: en cada ciclo se escriben las pruebas de los criterios, se guarda la evidencia en rojo y después se implementa y se guarda la evidencia en verde.
- Cada prueba lleva el requisito y el criterio en el nombre (por ejemplo `test_r04_ac05_...`).
- La regla de no doble reserva tiene prueba secuencial y prueba de solicitudes simultáneas.
- Fechas fijas y reloj inyectable, nunca la fecha del sistema.
- QA en el navegador con datos de prueba y capturas en `docs/evidencia-cN/`.
- Se corren y se anotan los resultados, con fecha, antes de cada PR y otra vez antes de presentar.

## Cambio de especificación
Se introduce a mitad del desarrollo (C3) y se documenta el ciclo completo: cambio pedido, spec con versión nueva, criterios, plan y tareas, pruebas en rojo, código, pruebas en verde y revisión de regresiones. La evidencia queda en `docs/` y en el historial de Git.

## Checklist de entrega
- [ ] Repositorio Git con estructura de referencia
- [ ] Issues y ramas por tarea
- [ ] Commits identificables
- [ ] Pull requests revisados por otra persona
- [ ] Pruebas automatizadas, con la prueba de no doble reserva
- [ ] Specs v1.0 y v1.1 con control de aprobación
- [ ] `docs/ai-log.md` con respuestas incorrectas y cambios rechazados, con evidencia
- [ ] `docs/decisions.md` y `docs/testing.md` al día
- [ ] README con comandos reales
- [ ] Stack declarado en `specs/architecture.md`
- [ ] Material de la presentación

## Riesgos
- Poco tiempo para siete ciclos desde cero.
- Que alguien del equipo no entienda una parte: el profesor elige al azar quién expone, así que los tres tenemos que entender todo.
- Que las pruebas de solicitudes simultáneas sean frágiles con SQLite.

## Supuestos y decisiones de Product

Confirmados por Emily el 2026-11-15 (D-011):
1. Horario de 07:00 a 22:00, hora de Panamá, con franjas de una hora y último inicio a las 21:00.
2. Reservas hasta hoy más 14 días calendario, inclusive.
3. Cancelación con al menos 2 horas de anticipación.

Decididos tras la revisión de Ivan (D-012 a D-016):
- Se cancela desde "Mis reservas" y desde la disponibilidad de la cancha, solo en reservas propias confirmadas.
- La disponibilidad de una fecha pasada o fuera de plazo se muestra, pero con las franjas como no reservables.
- Cancha inexistente o inactiva en la disponibilidad responde 404, el correo no distingue mayúsculas ni espacios en los extremos y "Mis reservas" muestra primero la más reciente.
- Cuentas: la opción más simple, el sistema de usuarios de Django tal cual, con el correo como nombre de usuario (D-015).
- Interfaz: HTML y CSS planos servidos por Django, sin librerías externas ni CDN (D-016).
- Lo que faltaría para hacer robusto lo anterior queda registrado en `docs/deuda-tecnica.md`.

Sigue por confirmar:
- Hora límite de la entrega del lunes, en hora de Panamá. La confirma Emily antes del cierre (C6).
