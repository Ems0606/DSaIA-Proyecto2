# Ajustes de Iván en #18 (AC28): rojo y verde

Fecha: 2026-11-15 (hora de Panamá). Comandos reales de `manage.py test` y `coverage`.

## Rojo (antes del cambio)

Pruebas nuevas: sin `fecha` muestra hoy con 200; `HEAD` responde como GET; POST sin token responde 405 con CSRF activo.

```text
FAIL: test_ac28_head_responde_como_get
AssertionError: 400 != 200
FAIL: test_ac28_post_responde_405_aunque_no_traiga_token_csrf
AssertionError: 403 != 405
FAIL: test_ac28_sin_parametro_fecha_muestra_hoy_en_panama_con_200
AssertionError: 400 != 200
Ran 16 tests in 0.041s
FAILED (failures=3)
```

## Verde (después del cambio)

Cambio: sin el parámetro `fecha` se usa la fecha de hoy en Panamá; una fecha vacía o inválida sigue en 400 (AC03); la vista es `csrf_exempt` porque solo admite GET y HEAD, así `require_safe` responde 405 a un POST sin token.

```text
Ran 33 tests in 0.065s
OK
TOTAL    99    2    98%
System check identified no issues (0 silenced).
No changes detected
```
