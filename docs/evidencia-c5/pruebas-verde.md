# Evidencia en verde de C5, parte 1 (2026-11-15)

Resultados reales de esta corrida, sobre main en `d0933b2` (con la spec v1.1 ya fusionada):

| Comprobación | Resultado |
|---|---|
| `python manage.py check` | sin incidencias |
| `python manage.py makemigrations --check --dry-run` | sin cambios pendientes (no hay migración nueva) |
| `python manage.py test` | 77 pruebas OK: 65 anteriores y 12 nuevas de C5 |
| Cobertura (`coverage run manage.py test`) | 97 % sobre `src/reservas` (251 de 260 líneas), meta 70 % |
| `python scripts/verificar_trazabilidad.py` | `R=13 BR=15 AC=35`, sin inconsistencias |

Las 12 pruebas nuevas estaban en rojo antes del código (`pruebas-rojo.md`).

## Comprobé que las pruebas pueden fallar

Rompí el código a propósito en una copia y corrí `tests.test_c5_mis_reservas`:

| Cambio hecho a propósito | Resultado |
|---|---|
| No filtrar las reservas por usuario | 3 fallas |
| Desempate con el ID menor primero | 1 falla |
| Quitar la exigencia de sesión | 1 error |
| Orden ascendente por inicio | 2 fallas |

Con el código restaurado, las 12 pasan.

## Lo que queda fuera

- **AC27 en "Mis reservas":** el botón de cancelar se agrega cuando el endpoint de C4 esté en main. Esta parte no cierra el issue #10.
- **AC19 completo** (ver mis reservas sin Internet): se comprueba en la QA con capturas. Hoy solo se comprobó por prueba automática que la página no pide recursos externos.
- **Apariencia:** no la revisé en un navegador; las pruebas comprueban contenido y orden, no el diseño.
