# Plan de implementación

Propuesta C0 (#3). El reparto de responsables, revisión y QA sigue [la planificación](../docs/planificacion.md). Los criterios y la trazabilidad siguen en borrador hasta que Product cierre los supuestos y se resuelva #13.

| Ciclo / issue | Trabajo y dependencia | Verificación de salida |
|---|---|---|
| C0 / #3 | Arquitectura, modelo, rutas y secuencia; revisión por Emily y QA por Rey. | El diseño cubre zona civil, integridad y dependencias; identificar pendientes sin aprobar v1.0. |
| C0 / #4 | Proyecto ejecutable desde raíz; CI, prueba de humo y documentación. Puede validarse en paralelo a #3. | Django carga, SQLite migra, Django Test y coverage.py corren localmente y en CI. |
| C1 / #5 | Tras la base C0, crear catálogo y consultar ocupación por fecha civil. C1 puede empezar sin reservas persistidas: la consulta de ocupación se prueba con una fuente controlada; en C2 se conecta al modelo real. | AC01–AC03 en rojo/verde; repetir AC02 con SQLite y reservas persistidas en C2. Confirmar primero la regla para canchas inactivas y fechas no reservables. |
| C2 / #6 y #7 | Usuario y registro si se confirman, persistencia de reservas, validaciones, índice parcial, transacciones e integración con la consulta de C1. | AC04–AC10, AC16–AC18 y AC20, incluido conflicto simultáneo con SQLite en archivo; repetir disponibilidad y documentar QA. |
| C3 / #8 | Introducir el cambio de spec v1.1 cuando v1.0 permita reservar y pase su regresión. Registrar solicitud, decisión, criterios, plan y tareas antes del código. | Evidencias en rojo y verde, criterios nuevos y control de aprobación; revisar al menos fronteras de la semana, concurrencia y compatibilidad con datos preexistentes cuando se defina la regla. |
| C4 / #9 | Cancelación con permisos y plazo; liberar la franja conservando historial. | AC11–AC14 y regresión de AC17–AC18, además de revalidar la v1.1 tras liberar una reserva. |
| C5 / #10 | Historial privado; conservar estados y convertir fechas para la UI. | AC15, confirmar acceso anónimo y orden con Product; QA sin acceso a Internet para AC19. |
| C6 / #11 | Completar matriz, repetir suite, medir cobertura, README, evidencias y material de entrega. | Documentar cobertura real contra meta del 70 %, resultados y limitaciones. |

En cada ciclo: confirmar spec y criterios, agregar pruebas con sus IDs, registrar el fallo inicial y luego el resultado verde, actualizar matriz y evidencias, solicitar revisión y QA. El reloj fijo usa hora de Panamá en los casos de prueba y los datos son ficticios. Si se propone recortar HU-05, primero cambiar el alcance en la spec y la trazabilidad con aprobación de Product.
