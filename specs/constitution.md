# Constitución del proyecto

Principios que valen para todo el proyecto. Si algo los contradice, gana este documento.

1. **Stack:** Python 3.12 y Django 5.2 con SQLite. La lógica de reservas no depende de servicios externos.
2. **Sin Internet para la demo:** la interfaz no carga librerías desde un CDN. En el Proyecto 1 la demo dependía de Internet y no queremos repetirlo.
3. **Entradas inválidas:** toda entrada inválida se rechaza con un mensaje claro y no modifica ningún dato.
4. **Fechas deterministas:** la lógica de reservas recibe la hora actual como parámetro (reloj inyectable). Las pruebas usan fechas fijas y nunca la fecha del sistema. El servidor trabaja en UTC.
5. **Sin criterio, sin código:** no se implementa nada que no tenga un criterio de aceptación verificable.
6. **Orden de un cambio:** toda modificación de comportamiento actualiza primero la spec y los criterios, después las pruebas y al final el código.
7. **No doble reserva:** la regla se cumple también cuando dos solicitudes llegan a la vez, y tiene prueba automatizada.
8. **La IA ayuda, el equipo decide:** se pide una tarea por prompt. Ningún resultado de IA se da por validado sin evidencia independiente (pruebas corridas, diff revisado). Los prompts significativos, los errores de la IA y los cambios que rechazamos van en `docs/ai-log.md`.
9. **Datos ficticios y sin secretos** en el repo.
10. **Documentación al día:** cada PR actualiza lo que cambió, no se deja para el final.
