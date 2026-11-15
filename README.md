# DSaIA-Proyecto2: reservas de canchas deportivas

Proyecto 2 de Tópicos Especiales II (UTP, Prof. Regis Rivera). Es un sistema de reservas de canchas deportivas hecho con ODD (primero el resultado que queremos para el usuario) y SDD (después las especificaciones, el código y las pruebas).

**Equipo:** Emily (Ems0606), Ivan y Rey.

## Estado

C0: base de Django disponible. Las [especificaciones v1.0](specs/requirements.md) están en revisión. El catálogo, la autenticación y las reservas se desarrollan en los siguientes ciclos. Los acuerdos sobre cuentas e interfaz están en [decisiones](docs/decisions.md).

## Estructura
- `specs/`: outcomes, requisitos, reglas de negocio, arquitectura, modelo de datos, API, criterios de aceptación y plan de implementación
- `docs/`: registro de uso de IA (`ai-log.md`), decisiones (`decisions.md`) y pruebas (`testing.md`)
- `src/config/`: configuración Django; `src/reservas/`: aplicación web
- `tests/`: pruebas automatizadas

## Cómo correrlo

Requiere Python 3.12. Desde la raíz del repositorio:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

En Windows, usar `py -3.12 -m venv .venv` y activar con `.venv\Scripts\Activate.ps1` en PowerShell. Abrir [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para ver la portada. SQLite crea `db.sqlite3` localmente; no se sube al repo. La portada no usa recursos externos.

```bash
python manage.py test
python -m coverage run manage.py test
python -m coverage report
```

[Resultados y alcance de la cobertura](docs/testing.md).

## Cómo trabajamos
Issue o historia de usuario, rama, commits pequeños, PR con la plantilla del repo, revisión de otra persona, QA y merge. Nadie aprueba su propio PR.
