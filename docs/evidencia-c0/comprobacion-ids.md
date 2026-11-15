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
