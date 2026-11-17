# DSaIA-Proyecto2: reservas de canchas deportivas

Proyecto 2 de Tópicos Especiales II de la UTP con el profesor Regis Rivera. El sistema permite consultar franjas por cancha y fecha, crear una cuenta, iniciar sesión, reservar, cancelar y consultar «Mis reservas». El equipo usó ODD para definir el resultado para el jugador y SDD para convertirlo en especificaciones y pruebas.

**Equipo:** Emily (Ems0606), Ivan y Rey.

## Reglas de la versión 1.1

- Quince franjas de una hora, de 07:00 a 22:00 en Panamá. Se pueden reservar franjas futuras hasta 14 días calendario desde hoy, inclusive.
- Una cancha admite una sola reserva confirmada por franja. Cada cuenta admite dos confirmadas por semana de la franja, de lunes a domingo en Panamá. Las que ya empezaron cuentan y las canceladas liberan cupo.
- El dueño puede cancelar con al menos dos horas de anticipación. El historial conserva las reservas canceladas.
- Django sirve el HTML y CSS localmente. Después de instalar las dependencias, la demo funciona sin acceso a Internet.

## Inicio local

Se necesita Python 3.12. Ejecuta desde la raíz del repositorio:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo_canchas
python manage.py runserver
```

En PowerShell, crea el entorno con `py -3.12 -m venv .venv` y actívalo con `.\.venv\Scripts\Activate.ps1`. Los comandos siguientes son los mismos.

Abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/). La carga crea «Cancha 1» y se puede repetir sin duplicarla. SQLite guarda la base local en `db.sqlite3`. Usa cuentas ficticias para la demo. El [guion de demostración](docs/presentacion/demo.md) explica cómo mostrar el límite, la cancelación y la recuperación del cupo.

## Pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python -m coverage run manage.py test --noinput
python -m coverage report --fail-under=70
python scripts/verificar_trazabilidad.py
```

En C6 pasaron **112 pruebas**. La cobertura de líneas fue **97 %** en `src/reservas` sin migraciones (325 de 334 líneas), frente a una meta del 70 %. Consulta el [resultado final](docs/testing.md#c6-cierre), la [trazabilidad](docs/traceability.md) y la [prueba de navegador sin Internet](docs/evidencia-c6/navegador.md).

## Documentación y entrega

- [Outcomes](specs/outcomes.md), [requisitos](specs/requirements.md), [reglas de negocio](specs/business-rules.md) y [criterios](specs/acceptance-criteria.md).
- [Arquitectura](specs/architecture.md), [modelo de datos](specs/data-model.md), [contrato HTTP](specs/api.md) y [plan por ciclos](specs/implementation-plan.md).
- [Decisiones](docs/decisions.md), [registro de IA](docs/ai-log.md) y [presentación de cierre](docs/presentacion/Proyecto-2-Reservas-de-canchas.pptx).

`src/config/` contiene la configuración de Django, `src/reservas/` la aplicación y `tests/` la suite automatizada. Cada cambio pasa por un issue, una rama y un PR con revisión, QA y evidencia. Nadie aprueba su propio PR.
