# Evidencia en rojo de C5, parte 2 (2026-11-15)

Antes de agregar el botón de cancelar en "Mis reservas" escribí sus pruebas (`tests/test_c5_cancelar_desde_mis_reservas.py`) y comprobé que fallan. Esta parte cubre AC27 en esa pantalla y reutiliza el endpoint de C4 (D-017).

Comando: `python manage.py test tests.test_c5_cancelar_desde_mis_reservas`

Resultado en rojo: 3 pruebas, `FAILED (failures=3)`. Las tres fallan porque la pantalla todavía no ofrece ningún formulario de cancelar (`Couldn't find '/reservas/1/cancelar/'`).

| Prueba | Resultado en rojo |
|---|---|
| `test_ac27_el_boton_aparece_solo_en_confirmadas_propias_dentro_del_plazo` | FAIL |
| `test_ac27_luis_recibe_el_boton_de_la_suya_y_no_el_de_la_de_ana` | FAIL |
| `test_ac27_cancelar_desde_el_formulario_libera_la_franja_y_quita_el_boton` | FAIL |

En el primer intento dos pruebas pasaban sin sentido: la de Luis solo comprobaba que no hubiera botones (algo que cumple una pantalla sin botón alguno) y la de cancelar tomaba el token CSRF del formulario de salir, que ya está en la página, y llamaba al endpoint de C4, que ya funcionaba. Las reforcé: la de Luis exige además el botón de su propia reserva, y la de cancelar exige que el formulario salga en la pantalla antes de enviarlo. Con eso volvieron a fallar en rojo.

Criterios cubiertos: AC27 en "Mis reservas" (propias, confirmadas, dentro del plazo de 2 horas incluido el caso justo de 2 horas; ni ajenas, ni canceladas, ni fuera de plazo ni ya pasadas), con el token CSRF del propio formulario.
