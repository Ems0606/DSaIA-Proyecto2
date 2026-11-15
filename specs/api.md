# Contrato HTTP de la interfaz

Propuesta C0 (#3). Son rutas HTML de Django servidas en el mismo origen. Los formularios se envían como `application/x-www-form-urlencoded` con token CSRF; no existe una API JSON en v1.0.

| Método y ruta | Entrada / acceso | Resultado esperado | Criterios |
|---|---|---|---|
| GET `/canchas/` | Público | 200, catálogo de canchas de ejemplo | AC01, AC19 |
| GET `/canchas/<id>/disponibilidad/?fecha=AAAA-MM-DD` | Público; fecha local | 200, franjas de la fecha y su ocupación | AC01–AC03, AC19 |
| GET/POST `/cuentas/registro/` | Público; POST: nombre, correo y contraseña | GET 200; POST válido redirige al acceso; datos inválidos 400 con errores de campo | AC16; falta prueba de alta válida |
| GET/POST `/cuentas/entrar/` | Público; POST: correo y contraseña | GET 200; POST válido abre sesión y redirige a la ruta local de origen o al catálogo; credenciales inválidas 400 | R08; falta criterio explícito de acceso |
| POST `/canchas/<id>/reservas/` | Sesión; fecha local `AAAA-MM-DD`, hora `HH:MM` | Guarda una fila confirmada y redirige a disponibilidad con su confirmación | AC04–AC10, AC17–AC20 |
| POST `/reservas/<id>/cancelar/` | Sesión del dueño; ID en la URL | Cambia el estado y redirige a la disponibilidad con confirmación | AC11–AC14, AC17–AC19 |
| GET `/mis-reservas/` | Sesión | 200, historial propio con cancha, inicio en Panamá y estado. Propuesta de orden: inicio descendente y, en empate, ID descendente | AC15, AC19 |

Redirecciones tras POST válido: 303 a un GET. Una operación que falla no deja cambios parciales (AC18). Las páginas muestran mensajes de error en español.

| Situación | Respuesta |
|---|---|
| Formato inválido, hora fuera de la política o intento fuera del horizonte de reserva | 400, error de campo o mensaje de negocio |
| Falta iniciar sesión | 302 al login; después se vuelve solo a una página GET local segura. Una operación POST se vuelve a enviar explícitamente. |
| CSRF inválido | 403 |
| Cancha no existente o reserva inexistente o ajena | 404 sin revelar datos de terceros. Para una cancha inactiva en disponibilidad, se propone el mismo 404; Product debe confirmarlo. |
| Cancha inactiva al reservar, franja ocupada o cancelación inválida por estado/plazo | 409, mensaje de negocio; para franja ocupada, `franja_ocupada` |
| Método no admitido | 405 |
| Bloqueo de SQLite que agotó la espera | 503 con indicación de reintento |

Por confirmar antes de programar: tratamiento de fechas pasadas o fuera del horizonte en disponibilidad, casos de éxito y error de autenticación, equivalencia del correo y orden del historial. Si se muestran franjas fuera del plazo, diferenciar ocupación de posibilidad de reservar: una franja sin reserva puede seguir fuera de la política.
