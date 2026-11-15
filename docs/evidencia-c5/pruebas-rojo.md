# Evidencia en rojo de C5, parte 1 (2026-11-15)

Antes de escribir "Mis reservas" escribí sus pruebas (`tests/test_c5_mis_reservas.py`) y comprobé que fallan. Esta primera parte de C5 cubre AC15 y AC26. El botón de cancelar en esta pantalla (AC27) se agrega cuando el endpoint de C4 esté en main (D-017), así que no tiene pruebas todavía.

Comando: `python manage.py test tests.test_c5_mis_reservas`

Resultado en rojo: 12 pruebas, `FAILED (failures=8, errors=4)`. La ruta `/mis-reservas/` todavía no existía, así que cualquier petición daba 404.

| Prueba | Resultado en rojo |
|---|---|
| `test_ac15_ana_ve_solo_las_suyas_pasadas_y_futuras_confirmadas_y_canceladas_la_mas_reciente_primero` | FAIL |
| `test_ac15_con_el_mismo_inicio_va_primero_la_de_id_mayor` | ERROR |
| `test_ac15_el_historial_conserva_las_reservas_de_una_cancha_que_ya_no_esta_activa` | ERROR |
| `test_ac15_luis_no_ve_las_reservas_de_ana` | ERROR |
| `test_ac15_muestra_la_cancha_y_la_hora_de_panama_no_la_de_utc` | FAIL |
| `test_ac15_sin_reservas_muestra_un_mensaje_claro` | FAIL |
| `test_ac18_ver_mis_reservas_no_cambia_ninguna_reserva` | FAIL |
| `test_ac19_la_pagina_no_pide_recursos_externos` | FAIL |
| `test_ac26_despues_de_entrar_se_vuelve_a_mis_reservas` | ERROR |
| `test_ac26_sin_sesion_lleva_al_inicio_de_sesion_y_no_muestra_ninguna_reserva` | FAIL |
| `test_el_menu_ofrece_mis_reservas_solo_con_sesion` | FAIL |
| `test_mis_reservas_solo_admite_lectura_y_un_post_responde_405_aunque_no_traiga_token` | FAIL |

Dos pruebas (`test_ac18_ver_mis_reservas_no_cambia_ninguna_reserva` y `test_ac19_la_pagina_no_pide_recursos_externos`) pasaban en el primer intento sin tener sentido, porque una página 404 no cambia datos ni pide recursos externos. Las reforcé para que exijan una respuesta 200 y volvieron a fallar en rojo.

Criterios cubiertos: AC15, AC26, y las partes de AC18 y AC19 que se pueden comprobar sin navegador. AC19 completo, sin Internet, se comprueba en la QA con capturas.
