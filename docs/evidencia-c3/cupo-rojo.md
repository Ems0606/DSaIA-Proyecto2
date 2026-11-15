# C3 en rojo

Corrida del 15 de noviembre de 2026 sobre C2 y la spec v1.1 en `d0933b2`, antes de agregar el límite semanal.

```sh
python manage.py test tests.test_c3_limite_semanal tests.test_c2_reservar.ReservarTests.test_r13_ac30_ana_puede_tener_tres_reservas_en_semanas_distintas --noinput --verbosity 2
```

Resultado real: 9 casos, 6 fallos. AC29, AC30 (tercera), AC31, AC32 y AC34 devolvieron 303 en el intento que debía devolver 409. En AC35 ambos POST confirmaron.

```text
AssertionError: 303 != 409 : Couldn't retrieve content: Response code was 303 (expected 409)
AssertionError: Lists differ: [(303, False), (303, False)] != [(303, False), (409, True)]
Ran 9 tests in 1.147s
FAILED (failures=6)
```

Los otros tres casos pasaron: el cupo independiente de Luis, la prioridad de franja ocupada y las tres reservas en semanas distintas. Esta última sustituye deliberadamente AC20 de v1.0, que permitía tres en la misma semana.
