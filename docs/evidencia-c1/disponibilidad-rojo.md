# Evidencia en rojo de disponibilidad (C1, #5)

Corrida local del 15 de noviembre de 2026 (hora de Panamá), Python 3.12.3, Django 5.2.19, sobre la rama `ccr-91912035-mj0mkm`, antes de crear el dominio, el modelo `Cancha` y la vista.

Criterios cubiertos por estas pruebas: AC01, AC02 (con ocupación inyectada), AC03, AC21, AC22 y la frontera de AC23 en la consulta. Además, R01 (catálogo y carga demo) y BR07 (día 14 inclusive).

Comando:

```text
.venv/bin/python manage.py test --verbosity 2
```

Salida real (fragmentos relevantes):

```text
Synchronizing apps without migrations:
  Creating tables...
Running migrations:
  Applying contenttypes.0001_initial... OK
  ... (migraciones de auth y sessions, todas OK)
System check identified no issues (0 silenced).
tests.test_disponibilidad_dominio (unittest.loader._FailedTest.tests.test_disponibilidad_dominio) ... ERROR
tests.test_disponibilidad_vistas (unittest.loader._FailedTest.tests.test_disponibilidad_vistas) ... ERROR
test_inicio_renderiza_la_plantilla_del_proyecto (tests.test_scaffolding.ScaffoldingTests.test_inicio_renderiza_la_plantilla_del_proyecto) ... ok
test_sesion_se_puede_guardar_y_recuperar (tests.test_scaffolding.ScaffoldingTests.test_sesion_se_puede_guardar_y_recuperar) ... ok

ERROR: tests.test_disponibilidad_dominio
ImportError: Failed to import test module: tests.test_disponibilidad_dominio
  File "/home/user/DSaIA-Proyecto2/tests/test_disponibilidad_dominio.py", line 10, in <module>
    from src.reservas import dominio
ImportError: cannot import name 'dominio' from 'src.reservas'

ERROR: tests.test_disponibilidad_vistas
ImportError: Failed to import test module: tests.test_disponibilidad_vistas
  File "/home/user/DSaIA-Proyecto2/tests/test_disponibilidad_vistas.py", line 15, in <module>
    from src.reservas.models import Cancha
ModuleNotFoundError: No module named 'src.reservas.models'

Ran 4 tests in 0.004s

FAILED (errors=2)
```

Lectura honesta del rojo: las pruebas nuevas fallan porque sus módulos todavía no existen (error de importación), no por una aserción fallida. Las dos pruebas de scaffolding de C0 siguen en verde. Las aserciones de comportamiento se ejercitan recién al implementar, y su primer resultado real queda en `disponibilidad-verde.md` junto con la corrección de lo que haga falta.
