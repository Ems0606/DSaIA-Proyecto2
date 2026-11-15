# Plan de implementación

Propuesta C0 (#3). El reparto de responsables, revisión y QA sigue [la planificación](../docs/planificacion.md). El plan incorpora D-011 a D-017; #13 contiene los criterios de la v1.0.

| Ciclo / issue | Trabajo y dependencia | Verificación de salida |
|---|---|---|
| C0 / #3 | Arquitectura, modelo, rutas y secuencia; revisión por Emily y QA por Rey. | El diseño cubre zona civil, integridad, dependencias y decisiones D-011 a D-017. |
| C0 / #4 | Proyecto ejecutable desde raíz; CI, prueba de humo y documentación. Puede validarse en paralelo a #3. | Django carga, SQLite migra, Django Test y coverage.py corren localmente y en CI. |
| C1 / #5 | Tras la base C0, crear el catálogo y consultar ocupación y posibilidad de reservar por fecha civil. Si la consulta de ocupación se prueba con una fuente controlada en C1, integrarla con reservas persistidas en C2. | AC01–AC03, AC21 y AC22 en rojo/verde. Repetir AC02 con SQLite y reservas persistidas en C2. |
| C2 / #6 y #7 | Registro y acceso con `auth.User`, usando el correo normalizado como `username` (D-015). Crear la persistencia de reservas, el índice parcial y las transacciones, y conectarlos a la consulta de C1. | AC04–AC10, AC16–AC18, AC20 y AC23–AC25. Verificar el conflicto simultáneo con SQLite en archivo y completar el paso de cancelación de AC24 en C4. |
| C3 / #8 | Introducir el cambio de spec v1.1 cuando v1.0 permita reservar y pase su regresión. Registrar solicitud, decisión, criterios, plan y tareas antes del código. | Evidencias en rojo y verde, criterios nuevos y control de aprobación; revisar al menos fronteras de la semana, concurrencia y compatibilidad con datos preexistentes. Definido en D-019 a D-022: spec v1.1 con R13, BR15 y AC29 a AC35; Ivan implementa con pruebas en rojo primero y ajusta la prueba de AC20 de C2 como cambio deliberado; Rey hace la QA. |
| C4 / #9 | Cancelación con permisos y plazo; liberar la franja conservando historial. Crear el endpoint de cancelación y conectar el formulario desde disponibilidad (D-017). | AC11–AC14, cancelación de AC24 y caso de disponibilidad de AC27. Repetir AC17–AC18 y la regresión de v1.1 tras liberar una reserva (AC32 completo, cancelando por el endpoint). |
| C5 / #10 | Historial privado de más reciente a más antigua. Agregar el botón de cancelación en «Mis reservas» reutilizando el endpoint de C4 (D-017). | AC15 y AC26, y cierre de AC27 con la verificación del botón en ambas pantallas. QA sin acceso a Internet para AC19. |
| C6 / #11 | Completar matriz, repetir suite, medir cobertura, README, evidencias y material de entrega. | Documentar cobertura real contra meta del 70 %, resultados y limitaciones. |

Usar plantillas HTML y CSS planos servidos por Django según D-016. En cada ciclo: confirmar spec y criterios, agregar pruebas con sus IDs, registrar el fallo inicial y luego el resultado verde, actualizar matriz y evidencias, solicitar revisión y QA. El reloj fijo usa hora de Panamá en los casos de prueba y los datos son ficticios. Si se propone recortar HU-05, primero cambiar el alcance en la spec y la trazabilidad con aprobación de Product.
