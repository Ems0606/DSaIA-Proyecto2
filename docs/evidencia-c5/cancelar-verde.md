# Evidencia en verde de C5, parte 2 (2026-11-15)

Resultados reales de esta corrida, sobre C5 parte 1 ya al día con C4 (`main` en `2c484f0`):

| Comprobación | Resultado |
|---|---|
| `python manage.py check` | sin incidencias |
| `python manage.py makemigrations --check --dry-run` | sin cambios pendientes (no hay migración nueva) |
| `python manage.py test` | 103 pruebas OK: 100 anteriores y 3 nuevas |
| Cobertura (`coverage run manage.py test`) | 97 % sobre `src/reservas` (314 de 323 líneas), meta 70 % |

Las 3 pruebas nuevas estaban en rojo antes del código (`cancelar-rojo.md`).

## Qué hace la parte 2

`servicios.reservas_de_usuario(usuario, ahora)` marca cada reserva con `cancelable`: confirmada y con al menos 2 horas de plazo (BR08 y BR14, con la misma `dominio.puede_cancelar` de C4). La plantilla dibuja un formulario POST al endpoint de C4 solo en esas. No se cambió el endpoint: tras cancelar redirige a la disponibilidad de la cancha con la confirmación, como dice `specs/api.md`.

## Comprobé que las pruebas pueden fallar

Rompí el código a propósito en una copia y corrí `tests.test_c5_cancelar_desde_mis_reservas` y `tests.test_c5_mis_reservas`:

| Cambio hecho a propósito | Resultado |
|---|---|
| Ofrecer cancelar también en las ya canceladas | 2 fallas |
| Ignorar el plazo de 2 horas | 1 falla |
| Exigir más de 2 horas (el caso justo de 2 horas ya no cancela) | 1 falla |
| Mostrar el botón siempre | 2 fallas |
| Quitar el token CSRF del formulario de cancelar | 1 error |

En la primera vuelta tres roturas no se detectaron. Dos fueron mi error: el cambio cayó en la función de cancelar de C4 en vez de en la mía. La tercera era un hueco real de la prueba, que tomaba el token de otro formulario; la corregí para que lea el token dentro del formulario de cancelar. Con las roturas bien apuntadas, las cinco se detectan, y con el código restaurado pasan las 103.

## Lo que queda fuera

- **AC19 completo con la parte nueva** (cancelar sin Internet desde esta pantalla): se comprueba en la QA de Ivan con capturas.
- **Apariencia:** no la revisé en un navegador; las pruebas comprueban contenido y comportamiento, no el diseño.
