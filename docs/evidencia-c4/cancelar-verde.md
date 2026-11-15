# Evidencia en verde de C4 (2026-11-15, 22:25 UTC)

Después de escribir las pruebas en rojo (`cancelar-rojo.md`), implementé lo mínimo: el dominio del plazo (`dominio.puede_cancelar`), la reserva propia en la disponibilidad, el caso de uso `servicios.cancelar`, la vista `cancelar` con su ruta `/reservas/<id>/cancelar/` y el botón en la plantilla de la disponibilidad.

## Pruebas de C4

Comando: `.venv/bin/python manage.py test tests.test_c4_cancelar`

Resultado real: `Ran 20 tests in 8.331s` y `OK`. Las 13 que fallaban en rojo ahora pasan y las 7 de guarda siguen en verde.

## Suite completa

Comando: `.venv/bin/python manage.py test`

Resultado real: `Ran 85 tests in 19.057s` y `OK`. Son 65 de la línea base (C0, C1 y C2, sin cambios) y 20 nuevas de C4.

## Verificaciones de configuración y migraciones

| Comando | Resultado real |
|---|---|
| `.venv/bin/python manage.py check` | `System check identified no issues (0 silenced).` (salida 0) |
| `.venv/bin/python manage.py makemigrations --check --dry-run` | `No changes detected` (salida 0). No hubo cambios de modelo en C4 y no se creó migración. |
| `.venv/bin/python manage.py migrate --noinput` | `Applying reservas.0002_reserva... OK` (salida 0). Se aplicó sobre la base local `db.sqlite3`, que no está versionada; la base local todavía estaba en `0001`. |

## Concurrencia de C2

Comando: `.venv/bin/python manage.py test tests.test_c2_concurrencia`, ejecutado 3 veces.

Resultado real: `OK` en las 3 corridas (`tests.test_c2_concurrencia`, la prueba de AC06 con dos hilos sobre SQLite de archivo).

## Criterios cubiertos en verde

| Criterio | Pruebas (en `tests/test_c4_cancelar.py`) |
|---|---|
| AC11 | `ac11_cancelar_deja_la_reserva_cancelada...`, `ac11_la_confirmacion...`, `ac11_la_franja_queda_libre_y_luis_puede_reservarla_sin_duplicar` |
| AC12 | 16:30 rechaza (409); 16:00 permite (303); reserva ya empezada rechaza |
| AC13 | Luis recibe 404 sin datos de Ana; reserva inexistente 404 |
| AC14 | Segunda cancelación: 409 "ya está cancelada" y no cambia `cancelada_en` |
| AC17 | Sin sesión: 302 a `/cuentas/entrar/` y sin cambios |
| AC18 y BR12 | Los rechazos no cambian ninguna reserva |
| AC27 (disponibilidad) | Botón solo en la propia, confirmada y dentro de plazo; no en ajena, cancelada ni fuera de plazo |
| CSRF | Sin token: 403 y sin cambios; con el token de la página: 303 |
| Método | GET a la ruta: 405 |
| api.md (503) | Bloqueo de SQLite agotado: 503 y sin cambios |

## Pendiente (no es de C4)

- AC19 (sin conexión) es de QA en el navegador.
- AC27 en «Mis reservas» es de C5 (D-017).
