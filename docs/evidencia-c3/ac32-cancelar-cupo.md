# AC32 por el endpoint de cancelación

Regresión de C3 y C4 verificada el 15 de noviembre de 2026. Con el reloj fijo al 16/11 a las 10:00 de Panamá, se crean por HTTP dos reservas confirmadas de Ana en la misma semana. Una tercera solicitud para otra franja recibe 409 con `limite_semanal`. El POST al endpoint de cancelación devuelve 303, conserva la fila cancelada y deja una confirmada. Repetir la tercera solicitud devuelve 303. Quedan dos confirmadas y una cancelada.

```sh
python manage.py test tests.test_c4_cancelar_integracion.CancelarCupoSemanalTests --noinput
```

- En `25bac63` (C4 y C5 parte 1, antes de C3), la prueba falló en la tercera solicitud con `303 != 409`. Ese resultado reproduce la ausencia del límite semanal.
- Tras integrar ese `main` en C3, pasó la prueba específica y la suite completa de **109 pruebas**. Cobertura de la app **97 %** (322 de 331 líneas). Sin migraciones pendientes.
