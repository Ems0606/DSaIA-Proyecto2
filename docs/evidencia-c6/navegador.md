# Flujo final de navegador sin Internet

Corrida de Ivan del 15 de noviembre de 2026 sobre el código de `e4146db` y el texto de portada actualizado para C6. Chrome 143.0.7499.170 contra Django en `127.0.0.1`, con base SQLite nueva y reloj fijo al 16/11/2026 a las 10:00 de Panamá. El contexto del navegador permitió solo el origen local y se verificó que un destino externo de control fallara.

Ana abrió la disponibilidad, se registró e inició sesión. Confirmó dos reservas en la misma semana. La tercera recibió 409 con `limite_semanal`. Desde «Mis reservas» canceló la de las 12:00 a exactamente dos horas de su inicio. La franja volvió a estar libre y al repetir la tercera solicitud obtuvo una confirmación. En el historial aparecieron dos confirmadas y una cancelada con la hora local. Así se comprobaron los flujos de AC19 con C3, C4 y C5 integrados, y se volvió a comprobar AC32 y el botón de AC27.

- [Límite semanal alcanzado](cupo-agotado.png).
- [Historial final con dos confirmadas y una cancelada](historial-final.png).

Salida real:

```text
Chrome 143.0.7499.170 Control ["https://qa-control.invalid/","net::ERR_INTERNET_DISCONNECTED"]
Consulta sin fecha 200: 16/11, 15 franjas. CSS local 200.
Altas y acceso 303. Dos primeras reservas 303/303. Tercera 409 limite_semanal.
Cancelar a dos horas desde Mis reservas: 303. Reintento de la tercera: 303. Historial 200.
SQLite: 2 confirmadas, 1 cancelada
Peticiones externas de la app: 0.
```
