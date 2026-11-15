# QA de C2 en navegador

El 15 de noviembre de 2026, Ivan verificó el [PR #19](https://github.com/Ems0606/DSaIA-Proyecto2/pull/19) en el commit `056587527e5798c014e929d2d777a8bc7b238285`. Pasaron todos los casos de la funcionalidad entregada en C2. Cancelación y «Mis reservas» completan los criterios compartidos en C4 y C5.

La corrida usó Chrome 143.0.7499.170, Python 3.12.16, Django 5.2.19 y SQLite 3.53.1. Migré una base nueva en un checkout aislado, cargué la cancha demo y agregué una cancha inactiva y otra activa para probar el plazo sin compartir la franja de AC09. Ana y Luis usaron sesiones independientes de Chrome. Fijé el reloj de la aplicación en el 16/11/2026 a las 10:00 de Panamá y en el 17/11 a las 02:30 UTC para AC23. `python manage.py test --noinput` pasó las 65 pruebas, incluida la prueba de concurrencia con barrera sobre SQLite en archivo.

| Criterio | Resultado observado | Captura |
|---|---|---|
| AC04 y parte persistida de AC02 | Ana reservó la cancha 1 el 17/11 a las 18:00. El POST devolvió 303, la página mostró la confirmación y la franja quedó ocupada. SQLite guardó una fila confirmada para Ana, a las 23:00 UTC. | [Reserva confirmada](qa-ac04-reserva.png) |
| AC05 | Ana y Luis abrieron la misma franja libre en dos ventanas con sesiones independientes. Ana reservó primero y Luis envió el formulario que ya tenía abierto. Luis recibió 409, con `franja_ocupada`. La única reserva confirmada siguió siendo la de Ana. | [Conflicto en la ventana de Luis](qa-ac05-conflicto.png) |
| AC06 | En otra franja libre, 17/11 a las 19:00, lancé los dos envíos en paralelo desde Chrome. Ana recibió 303 y Luis 409. SQLite registró una sola fila confirmada para ese inicio. | [Ventana de Ana](qa-ac06-confirmada.png), [ventana de Luis](qa-ac06-conflicto.png) |
| AC07 | El 18/11, 06:00, 22:00 y 18:30 devolvieron 400. Los inicios de las 07:00 y las 21:00 devolvieron 303. | [Rechazo de las 18:30](qa-ac07-hora-invalida.png) |
| AC08 | El 16/11, las 09:00 y las 10:00 devolvieron 400. Las 11:00 devolvieron 303. | [Rechazo de la hora actual](qa-ac08-inicio-pasado.png) |
| AC09 | El 30/11 a las 21:00 devolvió 303. El 01/12 a las 07:00 devolvió 400. El primer caso supera 336 horas y queda dentro del día calendario 14. | [Rechazo del 01/12](qa-ac09-fuera-del-plazo.png) |
| AC10 | POST a una cancha inactiva devolvió 409 con mensaje claro. Una cancha inexistente devolvió 404. Las reservas quedaron iguales. | [Cancha inactiva](qa-ac10-cancha-inactiva.png) |
| AC16 | Nombre vacío o de solo espacios, correo mal formado, correo duplicado con mayúsculas y espacios y contraseña de siete caracteres devolvieron 400 con su mensaje. SQLite conservó las mismas cuentas. | [Correo duplicado](qa-ac16-correo-duplicado.png) |
| AC17, parte de C2 | La disponibilidad para un visitante ofreció iniciar sesión. El POST de reserva sin sesión y con token CSRF válido redirigió al acceso con 302 y dejó las reservas iguales. El intento de cancelar sin sesión se verifica en C4. | [Acceso requerido](qa-ac17-sin-sesion.png) |
| AC18, rechazos de C2 | Comparé las filas de SQLite antes y después de los rechazos de horario, plazo, cancha, sesión y conflicto. Sus valores se conservaron. | Capturas de los rechazos arriba |
| AC19, parte de C2 | En un contexto de Chrome que permitía solo el origen local, disponibilidad y CSS cargaron con 200. El acceso y la reserva funcionaron con POST 303. Se vio la confirmación y la franja ocupada. | [Reserva con tráfico restringido a localhost](qa-ac19-reserva-sin-internet.png) |
| AC20 | Ana reservó a las 17:00 del 17, 18 y 19/11. Los tres POST devolvieron 303 y SQLite conservó las tres filas confirmadas en la misma semana. | [Tercera reserva](qa-ac20-tercera-reserva.png) |
| AC23 | A las 02:30 UTC del 17/11 seguía siendo el 16/11 en Panamá. El 30/11 a las 21:00 devolvió 303 y el 01/12 a las 07:00 devolvió 400. | [Último inicio del día 14](qa-ac23-dia-local.png) |
| AC24, parte de C2 | El alta de Ana devolvió 303 y se pudo iniciar sesión con el correo en mayúsculas. Después del acceso, reservó con esa sesión y el registro de AC04 quedó a su nombre. La cancelación se verifica en C4. | [Alta de Ana](qa-ac24-alta.png), [reserva con su sesión](qa-ac04-reserva.png) |
| AC25 | Contraseña incorrecta y correo inexistente devolvieron 400 y mostraron exactamente el mismo mensaje. El navegador siguió anónimo y no recibió cookie de sesión. | [Mensaje de acceso inválido](qa-ac25-acceso-invalido.png) |

Probé los rechazos del servidor desde el navegador con los formularios de la app. Para los valores que el formulario ya limita, suministré los datos inválidos en ese formulario o desactivé su validación HTML durante el caso, conservando la validación del servidor.

Para AC19 apliqué el bloqueo en el navegador y dejé el servidor en `127.0.0.1`. La navegación de control a `https://qa-control.invalid/` falló con `ERR_INTERNET_DISCONNECTED`. Durante el flujo de la app se observaron cero peticiones a destinos externos. Chrome no permitió capturar la página de la navegación abortada en el primer intento. Repetí el caso en un contexto nuevo y guardé la captura del flujo de la app. AC19 se completa al comprobar también cancelación y «Mis reservas» en C4 y C5.
