# Suite final de C6

15 de noviembre de 2026. Base de `main` con C0 a C5 en `e4146db57460f7f9ef86a0ff065037b40ec12a80`. Entorno Python 3.12.16, Django 5.2.19, SQLite 3.53.1 y coverage.py 7.17.3.

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate --noinput
python manage.py cargar_demo_canchas
python manage.py cargar_demo_canchas
python -m coverage run manage.py test --noinput
python -m coverage report --fail-under=70
python scripts/verificar_trazabilidad.py
```

`check` no reportó incidencias. No había migraciones pendientes y todas se aplicaron en una base nueva. La primera carga creó Cancha 1 y la segunda confirmó que ya existía. Pasaron las 112 pruebas.

```text
Name                                                      Stmts   Miss  Cover   Missing
src/reservas/__init__.py                                      0      0   100%
src/reservas/cuentas.py                                      25      1    96%   29
src/reservas/dominio.py                                      63      0   100%
src/reservas/management/__init__.py                           0      0   100%
src/reservas/management/commands/__init__.py                  0      0   100%
src/reservas/management/commands/cargar_demo_canchas.py      10      0   100%
src/reservas/models.py                                       26      2    92%   19, 52
src/reservas/reloj.py                                         3      0   100%
src/reservas/servicios.py                                    73      1    99%   94
src/reservas/views.py                                       134      5    96%   80, 92-93, 124-125
TOTAL                                                       334      9    97%
R=13 BR=15 AC=35
OK: sin inconsistencias
```

Las 325 líneas cubiertas corresponden a la aplicación `src/reservas`, excluidas las migraciones. La medición superó la meta de 70 %. La suite incluye doble reserva, cupo concurrente y cancelación concurrente sobre SQLite en archivo, más AC32 por el endpoint.
