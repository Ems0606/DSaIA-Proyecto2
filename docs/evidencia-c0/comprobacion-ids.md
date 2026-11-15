# Comprobación de IDs de las specs v1.0 (C0)

Fecha: 2026-11-14. Salida real de las pasadas que se hicieron sobre el borrador antes de commitearlo.

**Pasada 1** (borrador original)
```
R: 12 BR: 12 AC: 19
PROBLEMAS:
 - BR sin uso en AC/requisitos: BR03
 - BR sin uso en AC/requisitos: BR10
 - R10 sin AC que lo cite
```

**Pasada 2** (después de citar BR03 y R10 en criterios existentes y de agregar AC20 para BR10)
```
R=12 BR=12 AC=20
PROBLEMAS:
 - R sin AC: R01
```

**Pasada 3** (después de citar R01 en AC01)
```
R=12 BR=12 AC=20
OK: sin inconsistencias
```

Desde entonces la comprobación vive en `scripts/verificar_trazabilidad.py`. La última corrida con ese script, el 2026-11-14, dio `R=12 BR=12 AC=20` y `OK: sin inconsistencias`.

## Pasada del 2026-11-15: verificación pareja por pareja

Ivan, en su revisión del #13, señaló que el script anterior solo comprobaba que los IDs existieran: seguiría dando OK aunque se intercambiaran los criterios entre filas de la trazabilidad. Es cierto. Se reescribió `scripts/verificar_trazabilidad.py` para comprobar cada fila contra `specs/acceptance-criteria.md`.

La primera corrida del script nuevo encontró un error real en la trazabilidad recién redactada: la fila de R01 incluía AC21, pero ese criterio no citaba R01. Se corrigió citando R01 en AC21 (R01 define el catálogo de canchas y su estado activo).

Salida real después de la corrección. La prueba negativa se hizo sobre una copia temporal, que no se commitea, cruzando AC05 y AC10 entre las filas de R04 y R05:

```
--- Script nuevo sobre las specs corregidas:
R=12 BR=14 AC=27
OK: sin inconsistencias
codigo de salida: 0

--- Prueba negativa (copia temporal con AC05 y AC10 cruzados entre las filas de R04 y R05)
    Script nuevo:
R=12 BR=14 AC=27
PROBLEMAS:
 - R04: AC10 está en su fila pero ese criterio no cita R04
 - R04: sus criterios citan BR09 pero falta en las reglas de la fila
 - R05: AC05 está en su fila pero ese criterio no cita R05
 - R05: BR09 está en su fila pero ninguno de sus criterios la cita
 - R05: sus criterios citan BR05 pero falta en las reglas de la fila
 - R04: falta AC05 en la trazabilidad (ese criterio cita R04)
 - R05: falta AC10 en la trazabilidad (ese criterio cita R05)
codigo de salida: 1
    Script anterior (el del PR #13) sobre la misma copia cruzada:
R=12 BR=14 AC=27
OK: sin inconsistencias
codigo de salida: 0
```

Lo que demuestra: el script nuevo detecta el cruce y el anterior no. Lo que no demuestra: que los criterios estén bien pensados, eso sigue siendo revisión humana.
