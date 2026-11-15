# Contrato HTTP de la interfaz

Propuesta C0 (#3). Son rutas HTML de Django servidas en el mismo origen. Los formularios se envían como `application/x-www-form-urlencoded` con token CSRF; no existe una API JSON en v1.0.

| Método y ruta | Entrada / acceso | Resultado esperado | Criterios |
|---|---|---|---|
| GET `/canchas/` | Público | 200, catálogo de canchas de ejemplo | AC01, AC19 |
| GET `/canchas/<id>/disponibilidad/` | Público, con `fecha=AAAA-MM-DD` opcional. Sin el parámetro, se usa la fecha actual de Panamá. | 200 para una cancha activa, con la fecha seleccionada y las franjas con su ocupación y posibilidad de reservar. Un parámetro presente con valor vacío, mal formado o imposible recibe 400. En fechas pasadas o fuera de plazo, las franjas libres figuran como no reservables | AC01–AC03, AC19, AC21, AC22, AC27 |
| GET/POST `/cuentas/registro/` | Público; POST: nombre, correo y contraseña | GET 200; POST válido redirige al acceso; datos inválidos 400 con errores de campo | AC16, AC24 |
| GET/POST `/cuentas/entrar/` | Público; POST: correo y contraseña | GET 200; POST válido abre sesión y redirige a la ruta local de origen o al catálogo; credenciales inválidas 400 con el mismo mensaje para correo inexistente o contraseña incorrecta | AC24, AC25 |
| POST `/canchas/<id>/reservas/` | Sesión; fecha local `AAAA-MM-DD`, hora `HH:MM` | Guarda una fila confirmada y redirige a disponibilidad con su confirmación | AC04–AC10, AC17–AC20, AC23, AC24 |
| POST `/reservas/<id>/cancelar/` | Sesión del dueño; ID en la URL. Disponibilidad lo usa desde C4, y «Mis reservas» reutiliza el mismo endpoint desde C5 (D-017) | Cambia el estado y redirige a disponibilidad con confirmación | AC11–AC14, AC17–AC19, AC24, AC27 |
| GET `/mis-reservas/` | Sesión | 200, historial propio con cancha, inicio en Panamá y estado. Orden por inicio descendente y, en empate, ID descendente | AC15, AC19, AC26, AC27 |

Redirecciones tras POST válido: 303 a un GET. Una operación que falla no deja cambios parciales (AC18). Las páginas muestran mensajes de error en español.

| Situación | Respuesta |
|---|---|
| Formato inválido, hora fuera de la política o intento fuera del horizonte de reserva | 400, error de campo o mensaje de negocio |
| Falta iniciar sesión | 302 al login; después se vuelve solo a una página GET local segura. Una operación POST se vuelve a enviar explícitamente. |
| CSRF ausente o inválido en una ruta que admite la operación de escritura | 403. Los primeros formularios POST se incorporan en C2. |
| Cancha inexistente, cancha inactiva al consultar disponibilidad o reserva inexistente o ajena | 404 sin revelar datos de terceros. |
| Cancha inactiva al reservar, franja ocupada o cancelación inválida por estado/plazo | 409, mensaje de negocio; para franja ocupada, `franja_ocupada`; para el límite de 2 reservas por semana, `limite_semanal` |
| Método no admitido en la ruta | 405. Las rutas de consulta de C1 admiten GET y HEAD, y rechazan POST con 405. |
| Bloqueo de SQLite que agotó la espera | 503 con indicación de reintento |

Al registrar e iniciar sesión se recortan los espacios de los extremos del correo y se convierte a minúsculas para usarlo como `username` de Django (D-014, D-015). La interfaz ofrece cancelar solo al dueño de la reserva confirmada que cumple el plazo. Se incorpora el botón en disponibilidad en C4 y en «Mis reservas» en C5 (D-017). Cada pantalla aplica BR14 y el endpoint vuelve a comprobar BR08.
