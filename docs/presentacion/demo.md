# Demostración del Proyecto 2

El equipo completo puede usar este guion. Practicar una vez con la computadora y el proyector de la exposición. La [presentación](Proyecto-2-Reservas-de-canchas.pptx) incluye notas con referencias a la spec y las evidencias.

1. Antes de la exposición, instalar dependencias, migrar, cargar «Cancha 1» y arrancar Django según el [README](../../README.md). Abrir `127.0.0.1:8000`. Usar una cuenta nueva para que la semana quede sin reservas previas.
2. Desde «Canchas», abrir «Cancha 1» sin escribir fecha. Mostrar que aparece el día actual en Panamá. Elegir tres franjas libres de la misma semana con más de dos horas de anticipación, dentro del horizonte de 14 días.
3. Crear la cuenta ficticia de Ana e iniciar sesión. Reservar dos franjas y mostrar una ocupada en disponibilidad. Intentar la tercera franja libre de la misma semana. Debe aparecer el mensaje `limite_semanal`.
4. Abrir «Mis reservas» y cancelar una confirmada propia que siga dentro del plazo. Mostrar el aviso y volver a intentar la tercera franja. Ahora debe confirmarse. Volver al historial y señalar las dos confirmadas y la cancelada.
5. Repetir la carga o el tramo de cancelación con acceso a Internet desconectado y el servidor local activo. Si falla el equipo de exposición, mostrar el [registro y las capturas de C6](../evidencia-c6/navegador.md).

Para explicar la concurrencia, mostrar la [prueba de C2](../evidencia-c2/qa-navegador.md) con una confirmación y un conflicto para la misma franja. Para explicar el cambio durante el proyecto, mostrar los [fallos esperados de C3](../evidencia-c3/cupo-rojo.md) y [AC32 en verde](../evidencia-c3/ac32-cancelar-cupo.md).

Si los datos de la demo se ven distintos de las capturas, comprobar el reloj y que las tres fechas caigan en la misma semana de Panamá. Las capturas de C6 usan el reloj fijo del 16/11/2026 a las 10:00.
