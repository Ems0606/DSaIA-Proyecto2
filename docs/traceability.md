# Trazabilidad

Relación requisito, criterio de aceptación, tarea, prueba y evidencia, separada por ciclo cuando la tarea cambia. Se completa ciclo a ciclo: las columnas de prueba y evidencia están pendientes hasta que exista el código. No se marca nada como cubierto sin una prueba corrida.

`scripts/verificar_trazabilidad.py` comprueba cada fila contra `specs/acceptance-criteria.md`: los criterios de la fila tienen que citar ese requisito, las reglas de la fila tienen que salir de esos criterios y, entre todas las filas de un requisito, tienen que estar todos los criterios que lo citan.

| Requisito | Reglas | Criterios | HU / ciclo | Prueba | Evidencia |
|---|---|---|---|---|---|
| R01 | BR01, BR02, BR09 | AC01, AC21 | HU-01 (C1) | pendiente | pendiente |
| R02 | BR01, BR02, BR04, BR06, BR07, BR09, BR13 | AC01, AC02, AC03, AC21, AC22, AC28 | HU-01 (C1) | pendiente | pendiente |
| R03 | BR03, BR10 | AC04, AC20 | HU-02 (C2) | `test_c2_reservar`: ac04 y ac20 | [evidencia C2](evidencia-c2/pruebas-verde.md) |
| R04 | BR05 | AC05, AC06 | HU-03 (C2) | `test_c2_reservar`: ac05; `test_c2_concurrencia`: ac06 | [evidencia C2](evidencia-c2/pruebas-verde.md) |
| R04 | BR05, BR08 | AC11 | HU-04 (C4) | `test_c4_cancelar`: ac11 | [evidencia C4](evidencia-c4/cancelar-verde.md) |
| R05 | | AC03 | HU-01 (C1) | pendiente | pendiente |
| R05 | BR01, BR02, BR06, BR07, BR09 | AC07, AC08, AC09, AC10, AC23 | HU-02 (C2) | `test_c2_reservar`: ac07 a ac10 y ac23 | [evidencia C2](evidencia-c2/pruebas-verde.md) |
| R06 | BR05, BR08, BR14 | AC11, AC12, AC13, AC14, AC27 (en la disponibilidad) | HU-04 (C4) | `test_c4_cancelar`: ac11 a ac14 y ac27 en la disponibilidad | [evidencia C4](evidencia-c4/cancelar-verde.md) |
| R06 | BR14 | AC27 (en "Mis reservas") | HU-05 (C5) | pendiente | pendiente |
| R07 | BR03 | AC15, AC26 | HU-05 (C5) | `test_c5_mis_reservas`: ac15 y ac26 | [evidencia C5](evidencia-c5/pruebas-verde.md) |
| R08 | BR11 | AC16, AC17, AC24, AC25 | HU-02 (C2) | `test_c2_cuentas`: ac16, ac24, ac25; `test_c2_reservar`: ac17 | [evidencia C2](evidencia-c2/pruebas-verde.md) |
| R08 | | AC26 | HU-05 (C5) | `test_c5_mis_reservas`: ac26 | [evidencia C5](evidencia-c5/pruebas-verde.md) |
| R09 | BR14 | AC19, AC27 | HU-01, HU-02, HU-04, HU-05 | pendiente | pendiente |
| R10 | BR06, BR07, BR08, BR13 | AC08, AC09, AC12, AC22, AC23 | HU-01, HU-02, HU-04 | pendiente | pendiente |
| R11 | BR12 | AC18 | todos | pendiente | pendiente |
| R12 | | (cobertura) | C6 | pendiente | pendiente |
| R13 | BR15 | AC29, AC30, AC31, AC32, AC33, AC34, AC35 | HU-02 (C3); AC32 con el endpoint de cancelación, en C4 | pendiente | pendiente |
