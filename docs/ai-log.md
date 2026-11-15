# AI Development Log

Solo prompts significativos, con ID. Las respuestas incorrectas de la IA y los cambios que rechazamos se anotan tal cual pasaron. No se reescriben entradas previas; si algo queda obsoleto, se anota aparte.

Desde AI-004 solo se registran prompts de desarrollo, QA y producto o spec. AI-001 a AI-003 (organización inicial, 2026-11-14) se conservan tal como se escribieron.

| ID | Actividad | Herramienta IA | Qué se solicitó | Resultado | Decisión humana |
|---|---|---|---|---|---|
| AI-001 | Organizar el proyecto (2026-11-14) | Claude | Resumir el PDF del Proyecto 2, marcar lo ambiguo y proponer historias y reparto entre 3 | Resumen de entregables, 8 puntos ambiguos y una propuesta de 7 ciclos con roles rotativos | Emily eligió cancha deportiva, repo nuevo, el cambio de 2 reservas activas por semana y el alcance núcleo + Mis reservas; definió que un ciclo es una HU y fijó la entrega para el lunes 16 |
| AI-002 | Adaptar el Laboratorio 13 (2026-11-14) | Claude | Leer el Lab 13 y adaptar su proceso SDD al proyecto | La IA propuso constitución, spec versionada con aprobación, matriz de trazabilidad, pruebas en rojo antes de implementar y el ciclo del cambio de spec; también propuso añadir `specs/constitution.md` y `docs/traceability.md` | Pendiente de que el equipo confirme los dos archivos extra en el PR de planificación |
| AI-003 | Conectar GitHub (2026-11-14) | Claude | Usar `gh` y hacer push desde la VM Linux de la IA | **Respuesta incorrecta de la IA:** recomendó un login de dispositivo con `gh` en la VM, pero el sistema bloqueó la petición con un 403: "Cowork blocked this request: only git clone, git fetch and plain downloads from GitHub work here, not git push, other uploads or Git LFS. To push or upload, use a terminal on your own computer." La IA borró lo que había instalado | Emily decidió usar su Git Bash para push, PR y merge; la IA solo escribe archivos en la carpeta |
