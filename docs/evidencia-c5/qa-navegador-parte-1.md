# QA de «Mis reservas», parte 1

Ivan verificó el [PR #22](https://github.com/Ems0606/DSaIA-Proyecto2/pull/22) en `d72a2c72672b349208e9e41baf60306ac86175c1` el 15 de noviembre de 2026. Pasaron AC15, AC26 y la parte de «Mis reservas» de AC19. Las 77 pruebas automatizadas también pasaron.

Usé Chrome 143.0.7499.170 y un checkout con una base SQLite nueva. Fijé el reloj de Django al 16/11/2026 a las 10:00 de Panamá. Creé a Ana y Luis desde la pantalla de registro, usando sesiones independientes, y reservé dos franjas con cada cuenta. Preparé en SQLite una confirmada pasada y una cancelada de Ana para comprobar ambos estados en el historial.

| Criterio | Resultado observado | Evidencia |
|---|---|---|
| AC15, alcance, orden y hora | Ana vio solo sus cuatro reservas. Las dos del 20/11 a las 21:00 se ordenaron por ID descendente (primero Cancha QA 2). Después se mostró la cancelada del 19/11 y al final la confirmada del 15/11. Las 21:00 se mostraron en hora de Panamá, aunque ese instante corresponde al día siguiente a las 02:00 en UTC. | [Vista de Ana](qa-ac15-ana.png) |
| AC15, privacidad y estado | Luis vio únicamente sus dos confirmadas, del 20/11 a las 18:00 y del 18/11 a las 19:00, en ese orden. Las consultas conservaron las filas de SQLite. | [Vista de Luis](qa-ac15-luis.png) |
| AC26 | El GET anónimo a `/mis-reservas/` devolvió 302 al inicio de sesión con `next=/mis-reservas/`. La pantalla de acceso no mostró reservas. El POST de acceso devolvió 303 y Ana volvió a «Mis reservas». Antes de reservar, vio el mensaje de historial vacío. | [Acceso solicitado](qa-ac26-sin-sesion.png) |
| AC19, «Mis reservas» | En un contexto de Chrome limitado a `127.0.0.1`, la navegación externa de control falló con `ERR_INTERNET_DISCONNECTED`. La página del historial y su CSS local devolvieron 200, se mostraron las cuatro filas de Ana y la app no solicitó recursos externos. | [Historial sin acceso a Internet](qa-ac19-mis-reservas-local.png) |

La prueba del botón de cancelación de AC27 queda para la parte 2 de C5, después de integrar el endpoint de C4.
