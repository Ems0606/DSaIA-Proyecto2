# C3 en verde

Corrida del 15 de noviembre de 2026 con Python 3.12.16, Django 5.2.19 y SQLite 3.53.1. Se conservan los datos existentes. No hay cambios de migraciones.

```sh
python -m coverage run manage.py test --noinput
python -m coverage report
python manage.py makemigrations --check --dry-run
python scripts/verificar_trazabilidad.py
```

- 73 pruebas pasaron. Coverage.py midió 97 % sobre la app (255 de 263 líneas).
- AC35 pasó 10 de 10 corridas independientes sobre el archivo SQLite de pruebas. Los dos POST para franjas distintas dejaron una sola reserva nueva y un 409 con `limite_semanal`.
- La trazabilidad devolvió `R=13 BR=15 AC=35` y `OK: sin inconsistencias`.
- AC05 y AC06 siguen pasando. Ante un intento sobre una franja ya ocupada, se conserva `franja_ocupada` con prioridad sobre el cupo (D-022).
- AC20 de v1.0 se conserva como criterio histórico. La regresión vigente (AC30) conserva tres reservas de una persona el 16, 23 y 30/11, dentro del horizonte de 14 días, en semanas distintas.
- AC32 pasó con una cancelada preparada en SQLite. La [regresión por el endpoint de C4](ac32-cancelar-cupo.md) se verificó después de traer la cancelación desde main.
