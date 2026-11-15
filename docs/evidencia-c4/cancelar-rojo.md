# Evidencia en rojo de C4 (2026-11-15, 22:21 UTC)

Antes de implementar cancelar, escribí las pruebas de AC11, AC12, AC13, AC14, AC17, AC18 y AC27 (parte de la disponibilidad) en `tests/test_c4_cancelar.py` y las ejecuté contra el código de C2 sin cambios de C4.

Comando: `.venv/bin/python manage.py test tests.test_c4_cancelar -v 2`

Resultado real (última línea de la salida): `Ran 20 tests in 8.390s` y `FAILED (failures=13)`, sin errores. La prueba del 503 se añadió después de la primera corrida (ver la última fila de la tabla de rojo).

Pruebas en rojo (13). Fallan por aserción: la ruta `/reservas/<id>/cancelar/` todavía no existe, así que responde 404 donde se espera 303, 409 o 403, o no aparece el botón en la disponibilidad:

| Prueba | Criterio | Resultado en rojo |
|---|---|---|
| `test_ac11_cancelar_deja_la_reserva_cancelada_y_redirige_con_confirmacion` | AC11 | FAIL (`404 != 303`) |
| `test_ac11_la_confirmacion_de_cancelacion_se_muestra_en_la_disponibilidad` | AC11 | FAIL |
| `test_ac11_la_franja_queda_libre_y_luis_puede_reservarla_sin_duplicar` | AC11 | FAIL |
| `test_ac12_a_las_16_30_con_reserva_a_las_18_se_rechaza_y_sigue_confirmada` | AC12 | FAIL |
| `test_ac12_justo_a_las_16_00_con_reserva_a_las_18_todavia_se_permite` | AC12 | FAIL |
| `test_ac12_una_reserva_que_ya_empezo_no_se_puede_cancelar` | AC12 | FAIL |
| `test_ac14_cancelar_una_reserva_ya_cancelada_se_rechaza_con_mensaje_claro` | AC14 | FAIL |
| `test_ac17_sin_sesion_se_redirige_al_acceso_y_no_cambia_nada` | AC17 | FAIL |
| `test_cancelar_solo_admite_post` | R06 | FAIL |
| `test_post_sin_token_csrf_responde_403_y_no_cambia_nada` | BR12 | FAIL |
| `test_post_con_el_token_de_la_disponibilidad_cancela` | AC11 y CSRF | FAIL (no hay botón con token) |
| `test_503_si_sqlite_agota_la_espera_al_cancelar_y_no_cambia_nada` | api.md (503) | FAIL (la función `servicios.cancelar` aún no existe; el parche usa `create=True`) |
| `test_ac27_ana_ve_cancelar_en_su_reserva_confirmada_dentro_del_plazo` | AC27 | FAIL (no hay botón) |

Pruebas que ya pasan en rojo (7). Son de guarda: comprueban que algo no cambia o no se muestra, y hoy se cumplen porque la función aún no existe. Deben seguir en verde después de implementar:

| Prueba | Criterio | Resultado en rojo |
|---|---|---|
| `test_ac13_luis_no_puede_cancelar_la_reserva_de_ana_y_no_se_revelan_datos` | AC13 | ok (404 por ruta inexistente) |
| `test_ac13_una_reserva_inexistente_responde_404_y_no_cambia_nada` | AC13 | ok |
| `test_ac18_los_rechazos_no_cambian_ninguna_reserva` | AC18, BR12 | ok |
| `test_ac27_luis_ve_la_franja_ocupada_pero_no_ofrece_cancelar` | AC27 | ok |
| `test_ac27_un_visitante_sin_sesion_no_ve_cancelar` | AC27 | ok |
| `test_ac27_una_reserva_ya_cancelada_no_ofrece_cancelar` | AC27 | ok |
| `test_ac27_fuera_de_plazo_no_ofrece_cancelar` | AC27 | ok |

Las pruebas de C1 y C2 no se tocaron. La suite completa de la rama antes de C4 daba `Ran 65 tests ... OK`.
