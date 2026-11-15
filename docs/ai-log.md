# AI Development Log

Solo prompts significativos de desarrollo, QA y producto/spec, con ID. Lo administrativo (organización, configuración) no va aquí. Las respuestas incorrectas de la IA y los cambios que rechazamos se anotan tal cual pasaron. No se reescriben entradas previas; si algo queda obsoleto, se anota aparte.

| ID | Actividad | Herramienta IA | Qué se solicitó | Resultado | Decisión humana |
|---|---|---|---|---|---|
| AI-001 | Redactar las specs v1.0 (Product, 2026-11-14) | Claude | Redactar constitución, outcomes, requisitos, reglas de negocio, criterios de aceptación y trazabilidad de las reservas de canchas, con las decisiones que dimos | Borrador con 12 requisitos, 12 reglas y 20 criterios. **Respuesta incompleta de la IA:** el primer borrador tenía huecos de trazabilidad (BR03, BR10 y R10 sin criterio, y R01 sin cita en un criterio) que detectó una comprobación de IDs | La corrección la hizo la IA con esa comprobación, antes de commitear (evidencia: `docs/evidencia-c0/comprobacion-ids.md` y `scripts/verificar_trazabilidad.py`). Los supuestos de horario, duración, anticipación, cancelación y cuentas siguen pendientes de aprobación de Emily y revisión de Ivan |
