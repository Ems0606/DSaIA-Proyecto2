# Evidencia en verde de C2 (2026-11-15)

Rama de C2 apilada sobre #18 (C1) en su versión `4890e0f` (con main y el ajuste de AC28). Resultados reales de esta corrida:

| Comprobación | Resultado |
|---|---|
| `python manage.py check` | sin incidencias |
| `python manage.py makemigrations --check --dry-run` | sin cambios pendientes (la migración `0002_reserva` ya está incluida) |
| `python manage.py test` | 63 pruebas OK: 33 de C0 y C1, más 30 nuevas de C2 |
| Cobertura (`coverage run manage.py test`) | 96 % sobre `src/reservas` (239 de 248 líneas), meta 70 % |
| `python scripts/verificar_trazabilidad.py` | `R=12 BR=14 AC=28`, sin inconsistencias |

Las 30 pruebas nuevas estaban todas en rojo antes del código (`pruebas-rojo.md`).

## Concurrencia (AC06)

La prueba `test_ac06_dos_solicitudes_a_la_vez_dejan_una_sola_confirmada_y_un_conflicto` lanza dos hilos con barrera y su propio cliente sobre un archivo SQLite de prueba. Repetida 20 veces seguidas: 20 de 20 en verde, siempre con un 303 y un 409.

Comprobé que la prueba puede fallar. En una copia sin la comprobación previa ni el índice único parcial `reserva_confirmada_unica`, en 5 corridas las dos solicitudes devolvieron 303 y la prueba falló con `[303, 303] != [303, 409]` (junto con la de AC05). Es decir, las pruebas detectan que falta la protección.

## Lo que queda fuera

- AC19 (todo sin conexión a Internet) se comprueba en QA en el navegador con capturas, no con pruebas automáticas.
- AC02 con reservas persistidas queda cubierto por `test_ac04_la_franja_reservada_se_ve_ocupada`.
- Cancelar y "Mis reservas" son de C4 y C5.
- No probé con un SQLite bajo carga real, solo la competencia entre dos solicitudes.
