# Revisión de Iván en #23: cancelar en cancha desactivada (rojo y verde)

Iván probó que cancelar una reserva de una cancha ya desactivada devolvía 303 a `/canchas/<id>/disponibilidad/`, que responde 404, así que el jugador no veía la confirmación. El ajuste: para una cancha inactiva se vuelve a `/canchas/` (donde se muestra el aviso); para una cancha activa se mantiene el retorno a la disponibilidad.

Prueba nueva: `CancelarCanchaDesactivadaTests.test_ac11_cancelar_en_cancha_desactivada_vuelve_al_catalogo_con_la_confirmacion` en `tests/test_c4_cancelar_integracion.py`. Cambio de vista: `src/reservas/views.py`, función `cancelar`, bloque `if not reserva.cancha.activa: return _ver_otro(reverse("canchas"))`.

## Rojo

La vista original se verificó en una copia aislada del repositorio (en el directorio de trabajo del agente), no en la rama. En esa copia se restauró `src/reservas/views.py` a `HEAD` y se dejó el test nuevo.

Comando: `.venv/bin/python manage.py test tests.test_c4_cancelar_integracion.CancelarCanchaDesactivadaTests -v 2 --noinput`

Salida real (fragmento):

```
test_ac11_cancelar_en_cancha_desactivada_vuelve_al_catalogo_con_la_confirmacion (...) ... FAIL
FAIL: test_ac11_cancelar_en_cancha_desactivada_vuelve_al_catalogo_con_la_confirmacion (...)
  File ".../tests/test_c4_cancelar_integracion.py", line 112, in test_ac11_cancelar_en_cancha_desactivada_vuelve_al_catalogo_con_la_confirmacion
    self.assertEqual(respuesta["Location"], "/canchas/")
AssertionError: '/canchas/1/disponibilidad/?fecha=2026-11-17' != '/canchas/'
Ran 1 test in 0.217s
FAILED (failures=1)
```

## Verde

Comando: `.venv/bin/python manage.py test tests.test_c4_cancelar_integracion.CancelarCanchaDesactivadaTests -v 2 --noinput`

Salida real (fragmento):

```
test_ac11_cancelar_en_cancha_desactivada_vuelve_al_catalogo_con_la_confirmacion (...) ... ok
Ran 1 test in 0.207s
OK
```

## Suite completa

Comando: `.venv/bin/python manage.py test --noinput`

Salida real (fragmento): `Ran 88 tests in 20.231s` y `OK`. Código de salida 0.

## Cobertura

Comandos: `.venv/bin/python -m coverage run manage.py test --noinput` y `.venv/bin/python -m coverage report`

```
Name                                                      Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------
src/reservas/views.py                                       126      5    96%   79, 91-92, 117-118
TOTAL                                                       312      9    97%
```

Meta mínima 70 %: cumplida (97 %).

## Chequeos de calidad

- `.venv/bin/python manage.py check`: `System check identified no issues (0 silenced).`
- `.venv/bin/python manage.py makemigrations --check --dry-run`: `No changes detected`.
- `.venv/bin/python scripts/verificar_trazabilidad.py`: `R=13 BR=15 AC=35` y `OK: sin inconsistencias`.

## Pendiente de la revisión de Iván

AC32 de punta a punta (dos reservas, tercera rechazada con `limite_semanal`, cancelar una y reservar otra en la misma semana) depende del código de C3 (issue #8), que todavía no está en `main`. No se implementó en este PR.
