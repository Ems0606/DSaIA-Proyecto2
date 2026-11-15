# AC19 en C1: disponibilidad sin acceso a Internet

Verifiqué el [PR #18](https://github.com/Ems0606/DSaIA-Proyecto2/pull/18) en `4890e0f` el 15 de noviembre de 2026. Usé Chrome 143.0.7499.170 y Django en `127.0.0.1`, con la base migrada y la cancha de ejemplo de `python manage.py cargar_demo_canchas`.

El navegador bloqueó cualquier destino distinto del servidor local. La navegación de control falló con `ERR_INTERNET_DISCONNECTED`. El catálogo y la hoja de estilos local respondieron 200. No se observaron solicitudes externas de la app. Al abrir la Cancha 1 desde el catálogo y cambiar la fecha, se mostraron las 15 franjas con sus estados y estilos. [Captura de disponibilidad](ac19-disponibilidad-local.png).

Con el reloj a las 02:30 UTC del 17/11, abrir la cancha sin fecha devolvió 200 y seleccionó el 16/11 en Panamá. El POST sin token devolvió 405 con `Allow: GET, HEAD` y la fecha enviada vacía devolvió 400. La suite local pasó las 33 pruebas.
