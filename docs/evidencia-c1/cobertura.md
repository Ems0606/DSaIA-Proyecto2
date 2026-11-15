# Cobertura de disponibilidad (C1, #5)

Corrida local del 15 de noviembre de 2026 (hora de Panamá), Python 3.12.3, coverage.py 7.17.3. Medición con `.coveragerc` (fuente `src.reservas`, sin migraciones).

Comandos: `.venv/bin/python -m coverage run manage.py test` y `.venv/bin/python -m coverage report`.

Salida real de la corrida de pruebas:

```text
Found 30 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.082s

OK
Destroying test database for alias 'default'...
```

Salida real del reporte:

```text
Name                                                      Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------
src/reservas/__init__.py                                      0      0   100%
src/reservas/dominio.py                                      39      0   100%
src/reservas/management/__init__.py                           0      0   100%
src/reservas/management/commands/__init__.py                  0      0   100%
src/reservas/management/commands/cargar_demo_canchas.py      10      0   100%
src/reservas/models.py                                       11      1    91%   18
src/reservas/reloj.py                                         3      1    67%   10
src/reservas/servicios.py                                     7      0   100%
src/reservas/views.py                                        24      0   100%
---------------------------------------------------------------------------------------
TOTAL                                                        94      2    98%
```

Resultado: **98 %** del total de `src/reservas` (92 de 94 líneas ejecutables), contra la meta de 70 % (D-007).

Líneas sin cubrir:
- `src/reservas/models.py`, línea 18: el método `__str__` de `Cancha`. No lo usa ninguna prueba ni vista.
- `src/reservas/reloj.py`, línea 10: la lectura real del reloj `ahora()`. Las pruebas la parchean a propósito para fijar la hora (R10), así que esa línea solo se ejecuta en la operación real.

Alcance: la cobertura mide el código de C1. La ocupación de reservas persistidas (C2) todavía no existe, así que `inicios_ocupados` solo se prueba con datos inyectados.
