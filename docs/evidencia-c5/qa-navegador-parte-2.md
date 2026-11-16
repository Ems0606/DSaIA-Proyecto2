# QA del botón «Cancelar» en «Mis reservas»

Corrida de Ivan del 15 de noviembre de 2026 sobre `e16fe639f326c3b7d6a08c2a125256c3c6539b87` del [PR #26](https://github.com/Ems0606/DSaIA-Proyecto2/pull/26). Chrome 143.0.7499.170 contra un Django local con una base SQLite limpia. Se fijó el reloj al 16/11/2026 a las 10:00 de Panamá. Ana y Luis usaron sesiones independientes.

| Criterio | Resultado observado | Captura |
|---|---|---|
| AC27, botón según el plazo y estado | Ana vio el botón en sus dos confirmadas que cumplían el plazo, incluida la de las 12:00 a exactamente dos horas. Las de las 11:00 y 10:00, la del día anterior y una ya cancelada aparecieron sin botón. | [Historial de Ana antes de cancelar](qa-ac27-ana-cancelar.png) |
| AC27, privacidad | Luis vio solo su confirmada con su botón. Su historial no mostró la reserva de Ana, y el de Ana no mostró la de Luis. | [Historial de Luis](qa-ac27-luis-propia.png) |
| AC27, cancelar desde el historial | El formulario tenía su propio token CSRF y usó `POST /reservas/7/cancelar/`. Respondió 303 hacia disponibilidad, donde se mostró el aviso y la franja de las 12:00 volvió a estar libre. SQLite conservó la reserva como cancelada, con su fecha de cancelación. Al volver a «Mis reservas», la fila decía «Cancelada» y el botón había desaparecido. | [Franja liberada](qa-ac19-cancelacion-local.png), [historial tras cancelar](qa-ac27-cancelada-sin-boton.png) |
| AC19, cancelación sin Internet | En la sesión de Ana el navegador permitió solo el origen local. El control externo falló con `ERR_INTERNET_DISCONNECTED`. El historial y el CSS cargaron con 200, la cancelación devolvió 303 y la confirmación se mostró sin solicitudes externas de la app. | [Confirmación en la sesión restringida a localhost](qa-ac19-cancelacion-local.png) |

Registro real de la sesión restringida, con las solicitudes relevantes:

```text
Control https://qa-control.invalid/ -> net::ERR_INTERNET_DISCONNECTED
GET /mis-reservas/ 200
GET /static/reservas/estilo.css 200
POST /reservas/7/cancelar/ 303
GET /mis-reservas/ 200
SQLite: cancelada y cancelada_en guardado. Franja nuevamente libre; el historial quitó el botón.
```

`python manage.py test --noinput` dio 103 pruebas en verde. El script de trazabilidad reportó R=13, BR=15 y AC=35 sin inconsistencias.
