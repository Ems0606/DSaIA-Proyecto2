# Evidencia en rojo de C2 (2026-11-15)

Antes de escribir el código de reservar, registro y acceso, escribí las pruebas de C2 y comprobé que fallan. La rama parte de la de C1 (#18), así que las pruebas de disponibilidad siguen en verde.

Comando: `python manage.py test`

- Pruebas de C1 (disponibilidad y humo): 30, `OK`.
- Pruebas nuevas de C2: 30 (`tests/test_c2_cuentas.py`, `tests/test_c2_reservar.py` y `tests/test_c2_concurrencia.py`), todas fallan: `FAILED (failures=36, errors=4)`. El conteo es mayor que 30 porque las pruebas con `subTest` cuentan cada caso. Las fallas son 404 en las rutas que todavía no existen. Las que dan `ERROR` tocan el modelo `Reserva`, que aún no existe.

| Prueba | Resultado en rojo |
|---|---|
| `test_ac04_la_franja_reservada_se_ve_ocupada` | FAIL |
| `test_ac04_reservar_crea_una_reserva_confirmada_y_redirige_a_la_disponibilidad` | FAIL |
| `test_ac05_otro_usuario_en_la_misma_franja_recibe_conflicto` | FAIL |
| `test_ac06_dos_solicitudes_a_la_vez_dejan_una_sola_confirmada_y_un_conflicto` | FAIL |
| `test_ac07_horas_fuera_de_horario_o_no_en_punto_se_rechazan` | ERROR |
| `test_ac07_inicios_07_y_21_se_aceptan` | FAIL |
| `test_ac08_misma_fecha_a_las_09_y_a_las_10_se_rechaza` | FAIL |
| `test_ac08_misma_fecha_a_las_11_se_permite` | FAIL |
| `test_ac09_el_dia_30_a_las_21_se_permite_y_el_1_de_diciembre_se_rechaza` | FAIL |
| `test_ac10_cancha_inactiva_se_rechaza_con_conflicto` | FAIL |
| `test_ac10_cancha_inexistente_responde_404` | ERROR |
| `test_ac16_contrasena_de_7_caracteres_se_rechaza` | FAIL |
| `test_ac16_contrasena_de_8_caracteres_se_acepta` | FAIL |
| `test_ac16_correo_invalido_se_rechaza` | FAIL |
| `test_ac16_correo_repetido_con_otras_mayusculas_y_espacios_se_rechaza` | FAIL |
| `test_ac16_nombre_solo_espacios_se_rechaza` | FAIL |
| `test_ac16_nombre_vacio_se_rechaza_y_no_crea_usuario` | FAIL |
| `test_ac17_sin_sesion_pide_iniciar_sesion_y_no_crea_reserva` | FAIL |
| `test_ac18_un_rechazo_no_cambia_las_reservas_existentes` | ERROR |
| `test_ac20_ana_puede_tener_tres_reservas_confirmadas_a_la_vez` | FAIL |
| `test_ac23_con_las_21_30_de_panama_el_plazo_se_cuenta_desde_el_dia_de_panama` | FAIL |
| `test_ac24_acceso_sin_distinguir_mayusculas_ni_espacios_abre_sesion` | FAIL |
| `test_ac24_acceso_vuelve_a_la_ruta_local_de_origen` | FAIL |
| `test_ac24_registro_valido_guarda_correo_normalizado_y_redirige_al_acceso` | FAIL |
| `test_ac25_contrasena_incorrecta_se_rechaza_sin_abrir_sesion` | FAIL |
| `test_ac25_correo_inexistente_da_el_mismo_mensaje_que_contrasena_incorrecta` | FAIL |
| `test_acceso_no_sigue_una_ruta_externa_en_next` | FAIL |
| `test_fecha_con_formato_invalido_se_rechaza` | ERROR |
| `test_registro_get_muestra_el_formulario` | FAIL |
| `test_reservar_solo_admite_post` | FAIL |

Criterios cubiertos: AC04, AC05, AC06, AC07, AC08, AC09, AC10, AC16, AC17, AC18, AC20, AC23, AC24 y AC25. AC19 se comprueba en QA con capturas, no con pruebas automáticas.
