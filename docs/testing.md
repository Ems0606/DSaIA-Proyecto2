# Pruebas

## C0: base de Django (#4)

Corrida local del 15 de noviembre de 2026 con Python 3.12.16, Django 5.2.19, SQLite 3.53.1 y coverage.py 7.17.3.

| Comando o verificación | Resultado real |
|---|---|
| `python manage.py check` | Sin incidencias |
| `python manage.py makemigrations --check --dry-run` | Sin cambios pendientes |
| `python manage.py migrate --noinput` | Migraciones de auth, contenttypes y sessions aplicadas en SQLite |
| `python manage.py test` | 2 pruebas exitosas: portada y persistencia de sesión |
| `python -m coverage run manage.py test` y `python -m coverage report` | 100 % (5 de 5 líneas ejecutables de `src/reservas`, excluyendo migraciones) |
| `python manage.py runserver` y GET a la portada por loopback | HTTP 200, encabezado de la portada presente |

En rojo, antes de conectar la URL de inicio, la prueba de portada obtuvo 404 en lugar de 200 y la de sesión pasó. Después de conectar la ruta y la plantilla, ambas pasaron. [Evidencia de la corrida](evidencia-c0/scaffolding.md).

El workflow `Django CI` ejecuta verificación de configuración, migraciones y pruebas con cobertura en Python 3.12 para cada PR y push a `main`. El porcentaje de C0 mide la base de la app. La meta de 70 % se reevalúa con código de dominio en C6. C0 no cubre criterios de negocio; QA manual de los flujos se hará en sus ciclos y la aceptación de C0 queda con Rey.
