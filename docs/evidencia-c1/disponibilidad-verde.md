# Evidencia en verde de disponibilidad (C1, #5)

Corrida local del 15 de noviembre de 2026 (hora de Panamá), Python 3.12.3, Django 5.2.19, coverage.py 7.17.3, rama `ccr-91912035-mj0mkm`. Se cubre AC01, AC02 (con ocupación inyectada), AC03, AC21, AC22 y la frontera de AC23 en la consulta. La hora de las pruebas se fija parcheando `src.reservas.reloj.ahora`, y la ocupación se inyecta parcheando `src.reservas.servicios.inicios_ocupados`.

## Pruebas

Comando: `.venv/bin/python manage.py test --verbosity 2`

Salida real:

```text
Found 30 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: auth, contenttypes, reservas, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying reservas.0001_initial... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_r01_el_catalogo_muestra_solo_las_canchas_activas (tests.test_disponibilidad_vistas.CatalogoCanchasTests.test_r01_el_catalogo_muestra_solo_las_canchas_activas) ... ok
test_r01_la_carga_demo_es_repetible_y_no_duplica_canchas (tests.test_disponibilidad_vistas.CatalogoCanchasTests.test_r01_la_carga_demo_es_repetible_y_no_duplica_canchas) ... ok
test_ac01_sin_reservas_se_ven_15_franjas_todas_libres (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac01_sin_reservas_se_ven_15_franjas_todas_libres) ... ok
test_ac02_franja_ocupada_de_las_18_y_las_otras_14_libres (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac02_franja_ocupada_de_las_18_y_las_otras_14_libres) ... ok
test_ac03_fecha_con_formato_dd_mm_aaaa_responde_error_sin_franjas (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac03_fecha_con_formato_dd_mm_aaaa_responde_error_sin_franjas) ... ok
test_ac03_fecha_imposible_responde_error_sin_franjas (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac03_fecha_imposible_responde_error_sin_franjas) ... ok
test_ac03_sin_parametro_fecha_responde_error_sin_franjas (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac03_sin_parametro_fecha_responde_error_sin_franjas) ... ok
test_ac21_cancha_inactiva_responde_404_sin_franjas (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac21_cancha_inactiva_responde_404_sin_franjas) ... ok
test_ac21_cancha_inexistente_responde_404_sin_franjas (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac21_cancha_inexistente_responde_404_sin_franjas) ... ok
test_ac22_el_16_a_las_10_las_franjas_hasta_las_10_no_son_reservables_y_desde_las_11_si (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac22_el_16_a_las_10_las_franjas_hasta_las_10_no_son_reservables_y_desde_las_11_si) ... ok
test_ac22_fecha_fuera_de_plazo_se_ve_pero_ninguna_franja_es_reservable (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac22_fecha_fuera_de_plazo_se_ve_pero_ninguna_franja_es_reservable) ... ok
test_ac22_fecha_pasada_se_ve_pero_ninguna_franja_es_reservable (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac22_fecha_pasada_se_ve_pero_ninguna_franja_es_reservable) ... ok
test_ac23_el_plazo_se_cuenta_con_el_dia_de_panama (tests.test_disponibilidad_vistas.DisponibilidadVistaTests.test_ac23_el_plazo_se_cuenta_con_el_dia_de_panama) ... ok
test_inicio_renderiza_la_plantilla_del_proyecto (tests.test_scaffolding.ScaffoldingTests.test_inicio_renderiza_la_plantilla_del_proyecto) ... ok
test_sesion_se_puede_guardar_y_recuperar (tests.test_scaffolding.ScaffoldingTests.test_sesion_se_puede_guardar_y_recuperar) ... ok
test_ac03_acepta_la_fecha_en_formato_aaaa_mm_dd (tests.test_disponibilidad_dominio.FechaTests.test_ac03_acepta_la_fecha_en_formato_aaaa_mm_dd) ... ok
test_ac03_el_mensaje_de_error_indica_el_formato_esperado (tests.test_disponibilidad_dominio.FechaTests.test_ac03_el_mensaje_de_error_indica_el_formato_esperado) ... ok
test_ac03_rechaza_la_fecha_escrita_como_dd_mm_aaaa (tests.test_disponibilidad_dominio.FechaTests.test_ac03_rechaza_la_fecha_escrita_como_dd_mm_aaaa) ... ok
test_ac03_rechaza_una_fecha_imposible (tests.test_disponibilidad_dominio.FechaTests.test_ac03_rechaza_una_fecha_imposible) ... ok
test_ac03_rechaza_vacia_mal_formada_o_sin_ceros (tests.test_disponibilidad_dominio.FechaTests.test_ac03_rechaza_vacia_mal_formada_o_sin_ceros) ... ok
test_ac01_cada_franja_dura_una_hora (tests.test_disponibilidad_dominio.FranjasDelDiaTests.test_ac01_cada_franja_dura_una_hora) ... ok
test_ac01_hay_15_franjas_de_0700_a_2200_hora_de_panama (tests.test_disponibilidad_dominio.FranjasDelDiaTests.test_ac01_hay_15_franjas_de_0700_a_2200_hora_de_panama) ... ok
test_ac01_sin_reservas_todas_las_franjas_estan_libres (tests.test_disponibilidad_dominio.FranjasDelDiaTests.test_ac01_sin_reservas_todas_las_franjas_estan_libres) ... ok
test_ac02_la_franja_de_las_18_aparece_ocupada_y_las_otras_14_libres (tests.test_disponibilidad_dominio.OcupacionTests.test_ac02_la_franja_de_las_18_aparece_ocupada_y_las_otras_14_libres) ... ok
test_una_franja_ocupada_nunca_es_reservable (tests.test_disponibilidad_dominio.OcupacionTests.test_una_franja_ocupada_nunca_es_reservable) ... ok
test_ac22_el_16_a_las_10_las_franjas_hasta_las_10_no_son_reservables_y_desde_las_11_si (tests.test_disponibilidad_dominio.ReservabilidadTests.test_ac22_el_16_a_las_10_las_franjas_hasta_las_10_no_son_reservables_y_desde_las_11_si) ... ok
test_ac22_fecha_fuera_de_plazo_no_tiene_franjas_reservables (tests.test_disponibilidad_dominio.ReservabilidadTests.test_ac22_fecha_fuera_de_plazo_no_tiene_franjas_reservables) ... ok
test_ac22_fecha_pasada_no_tiene_franjas_reservables (tests.test_disponibilidad_dominio.ReservabilidadTests.test_ac22_fecha_pasada_no_tiene_franjas_reservables) ... ok
test_ac23_el_plazo_se_cuenta_con_el_dia_de_panama_y_no_con_utc (tests.test_disponibilidad_dominio.ReservabilidadTests.test_ac23_el_plazo_se_cuenta_con_el_dia_de_panama_y_no_con_utc) ... ok
test_br07_el_dia_14_es_reservable_inclusive (tests.test_disponibilidad_dominio.ReservabilidadTests.test_br07_el_dia_14_es_reservable_inclusive) ... ok

----------------------------------------------------------------------
Ran 30 tests in 0.037s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
EXIT=0
```

Resultado: 30 pruebas, 30 exitosas (las 2 de C0 y 28 nuevas).

Nota sobre las primeras corridas: cinco aserciones de AC03 fallaron (tres en la primera corrida y dos en la segunda) por un error de la propia prueba: `assertContains` y `assertNotContains` usan el código 200 por defecto y esas respuestas son 400. Se corrigió pasando `status_code=400`, sin cambiar criterios ni la aplicación. La salida de este archivo corresponde a la corrida posterior a la corrección.

## Verificaciones del repo

Salida real, en este orden: `check`, `makemigrations --check --dry-run`, `migrate --noinput`.

```text
$ .venv/bin/python manage.py check
System check identified no issues (0 silenced).
EXIT=0

$ .venv/bin/python manage.py makemigrations --check --dry-run
No changes detected
EXIT=0

$ .venv/bin/python manage.py migrate --noinput
Operations to perform:
  Apply all migrations: auth, contenttypes, reservas, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying reservas.0001_initial... OK
  Applying sessions.0001_initial... OK
EXIT=0
```

## QA manual con servidor local

Servidor de desarrollo (`manage.py runserver`) con la cancha de demo cargada con `manage.py cargar_demo_canchas`. Las respuestas HTTP son las observadas con curl:

| Petición | Código HTTP observado | Resultado |
|---|---|---|
| `GET /` | 200 | Portada |
| `GET /canchas/` | 200 | Catálogo con Cancha 1 |
| `GET /canchas/1/disponibilidad/?fecha=2026-11-17` | 200 | 15 franjas libres y reservables (HTML con franjas de 07:00-08:00 a 21:00-22:00) |
| `GET /canchas/1/disponibilidad/?fecha=2026-11-15` | 200 | Fecha pasada, sin franjas reservables |
| `GET /canchas/1/disponibilidad/?fecha=17/11/2026` | 400 | Mensaje: "La fecha debe escribirse como AAAA-MM-DD, por ejemplo 2026-11-17." Sin franjas |
| `GET /canchas/1/disponibilidad/?fecha=2026-02-30` | 400 | Mismo mensaje. Sin franjas |
| `GET /canchas/1/disponibilidad/` (sin `fecha`) | 400 | Mismo mensaje. Sin franjas |
| `GET /canchas/9999/disponibilidad/?fecha=2026-11-17` | 404 | Plantilla 404 en español con `DEBUG` apagado. Sin franjas |
| `POST /canchas/1/disponibilidad/` sin token CSRF | 403 | Lo rechaza el middleware CSRF antes de la vista |

Comprobaciones adicionales: la página no referencia URLs externas (ni CDN ni fuentes remotas), y `static/reservas/estilo.css` responde 200 como `text/css`.

Pendiente de QA: la prueba en un teléfono real o en una ventana estrecha del navegador (sin scroll horizontal) no se hizo; el CSS usa ancho máximo y envoltura flexible, pero no se verificó visualmente. Tampoco se probó AC19 (sin conexión), que corresponde a QA posterior.
