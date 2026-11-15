# Evidencia de pruebas de humo (C0, #4)

Corrida local, 2026-11-15 (hora de Panamá). Se muestran los fragmentos relevantes de la salida real.

Antes de conectar la portada, `python manage.py test --verbosity 2`:

```text
test_inicio_renderiza_la_plantilla_del_proyecto (tests.test_scaffolding.ScaffoldingTests.test_inicio_renderiza_la_plantilla_del_proyecto) ... FAIL
test_sesion_se_puede_guardar_y_recuperar (tests.test_scaffolding.ScaffoldingTests.test_sesion_se_puede_guardar_y_recuperar) ... ok

AssertionError: 404 != 200

Ran 2 tests in 0.003s

FAILED (failures=1)
```

Después de conectar la URL y crear la plantilla, `python manage.py test`:

```text
Ran 2 tests in 0.003s

OK
```

Tras `python -m coverage run manage.py test`, `python -m coverage report`:

```text
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src/reservas/__init__.py       0      0   100%
src/reservas/views.py          5      0   100%
--------------------------------------------------------
TOTAL                          5      0   100%
```

Comprobación adicional de `runserver` por loopback: `GET / HTTP 200; título de la portada presente`.
