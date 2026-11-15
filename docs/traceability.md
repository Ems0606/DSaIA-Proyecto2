# Trazabilidad

Relación requisito, criterio de aceptación, tarea, prueba y evidencia, separada por ciclo cuando la tarea cambia. Se completa ciclo a ciclo: las columnas de prueba y evidencia están pendientes hasta que exista el código. No se marca nada como cubierto sin una prueba corrida.

`scripts/verificar_trazabilidad.py` comprueba cada fila contra `specs/acceptance-criteria.md`: los criterios de la fila tienen que citar ese requisito, las reglas de la fila tienen que salir de esos criterios y, entre todas las filas de un requisito, tienen que estar todos los criterios que lo citan.

| Requisito | Reglas | Criterios | HU / ciclo | Prueba | Evidencia |
|---|---|---|---|---|---|
| R01 | BR01, BR02, BR09 | AC01, AC21 | HU-01 (C1) | pendiente | pendiente |
| R02 | BR01, BR02, BR04, BR06, BR07, BR09, BR13 | AC01, AC02, AC03, AC21, AC22, AC28 | HU-01 (C1) | pendiente | pendiente |
| R03 | BR03, BR10 | AC04, AC20 | HU-02 (C2) | pendiente | pendiente |
| R04 | BR05 | AC05, AC06 | HU-03 (C2) | pendiente | pendiente |
| R04 | BR05, BR08 | AC11 | HU-04 (C4) | pendiente | pendiente |
| R05 | | AC03 | HU-01 (C1) | pendiente | pendiente |
| R05 | BR01, BR02, BR06, BR07, BR09 | AC07, AC08, AC09, AC10, AC23 | HU-02 (C2) | pendiente | pendiente |
| R06 | BR05, BR08, BR14 | AC11, AC12, AC13, AC14, AC27 (en la disponibilidad) | HU-04 (C4) | pendiente | pendiente |
| R06 | BR14 | AC27 (en "Mis reservas") | HU-05 (C5) | pendiente | pendiente |
| R07 | BR03 | AC15, AC26 | HU-05 (C5) | pendiente | pendiente |
| R08 | BR11 | AC16, AC17, AC24, AC25 | HU-02 (C2) | pendiente | pendiente |
| R08 | | AC26 | HU-05 (C5) | pendiente | pendiente |
| R09 | BR14 | AC19, AC27 | HU-01, HU-02, HU-04, HU-05 | pendiente | pendiente |
| R10 | BR06, BR07, BR08, BR13 | AC08, AC09, AC12, AC22, AC23 | HU-01, HU-02, HU-04 | pendiente | pendiente |
| R11 | BR12 | AC18 | todos | pendiente | pendiente |
| R12 | | (cobertura) | C6 | pendiente | pendiente |
