# Cobertura de C4 (2026-11-15, 22:24 UTC)

Comandos: `.venv/bin/python -m coverage run manage.py test` y `.venv/bin/python -m coverage report`. La suite corrida fue la completa: `Ran 85 tests in 20.635s` y `OK`.

Meta del proyecto (D-007): 70 %. Resultado real: **97 %** (310 líneas, 9 sin ejecutar), con `source = src.reservas` y sin migraciones, según `.coveragerc`.

```
Name                                                      Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------
src/reservas/__init__.py                                      0      0   100%
src/reservas/cuentas.py                                      25      1    96%   29
src/reservas/dominio.py                                      63      0   100%
src/reservas/management/__init__.py                           0      0   100%
src/reservas/management/commands/__init__.py                  0      0   100%
src/reservas/management/commands/cargar_demo_canchas.py      10      0   100%
src/reservas/models.py                                       26      2    92%   19, 52
src/reservas/reloj.py                                         3      0   100%
src/reservas/servicios.py                                    59      1    98%   90
src/reservas/views.py                                       124      5    96%   79, 91-92, 117-118
---------------------------------------------------------------------------------------
TOTAL                                                       310      9    97%
```

Líneas sin ejecutar relacionadas con C4:

- `servicios.py` línea 90: la comprobación de respaldo `cambiadas != 1` en `servicios.cancelar`. Solo se alcanza si dos cancelaciones concurrentes llegan a la vez, y la prueba de C4 es secuencial. Es el caso que describe la arquitectura (punto 3) y no tiene prueba concurrente propia todavía.
- Las demás líneas sin ejecutar son de C1 y C2 (`entrar`, `salir`, `cuentas`, `models.__str__`, la rama 503 de `reservar`) y no las toqué.
