"""Pruebas HTTP de cuentas: registro, acceso y cierre de ciclo C2 (AC16, AC24, AC25).

Los usuarios son los del plan de pruebas: Ana y Luis. El correo es el `username` de
Django, normalizado con espacios recortados y en minúsculas (D-014, D-015).
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

REGISTRO = "/cuentas/registro/"
ENTRAR = "/cuentas/entrar/"
Usuario = get_user_model()


def datos_registro(**cambios):
    datos = {"nombre": "Ana Pérez", "correo": "ana@ejemplo.com", "contrasena": "clave-segura-1"}
    datos.update(cambios)
    return datos


class RegistroTests(TestCase):
    def test_ac16_nombre_vacio_se_rechaza_y_no_crea_usuario(self):
        respuesta = self.client.post(REGISTRO, datos_registro(nombre=""))

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_ac16_nombre_solo_espacios_se_rechaza(self):
        respuesta = self.client.post(REGISTRO, datos_registro(nombre="    "))

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_ac16_correo_invalido_se_rechaza(self):
        respuesta = self.client.post(REGISTRO, datos_registro(correo="ana-sin-arroba"))

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_ac16_contrasena_de_7_caracteres_se_rechaza(self):
        respuesta = self.client.post(REGISTRO, datos_registro(contrasena="abcdefg"))

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_ac16_contrasena_de_8_caracteres_se_acepta(self):
        respuesta = self.client.post(REGISTRO, datos_registro(contrasena="abcdefgh"))

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_ac16_correo_repetido_con_otras_mayusculas_y_espacios_se_rechaza(self):
        self.client.post(REGISTRO, datos_registro(correo="ana@ejemplo.com"))

        respuesta = self.client.post(REGISTRO, datos_registro(correo="  Ana@Ejemplo.com "))

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_ac24_registro_valido_guarda_correo_normalizado_y_redirige_al_acceso(self):
        respuesta = self.client.post(REGISTRO, datos_registro(correo="  Ana@Ejemplo.com "))

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(respuesta["Location"], ENTRAR)
        usuario = Usuario.objects.get()
        self.assertEqual(usuario.username, "ana@ejemplo.com")
        self.assertEqual(usuario.first_name, "Ana Pérez")
        self.assertTrue(usuario.check_password("clave-segura-1"))

    def test_registro_get_muestra_el_formulario(self):
        respuesta = self.client.get(REGISTRO)

        self.assertEqual(respuesta.status_code, 200)


class AccesoTests(TestCase):
    def setUp(self):
        Usuario.objects.create_user("ana@ejemplo.com", password="clave-segura-1", first_name="Ana")

    def test_ac24_acceso_sin_distinguir_mayusculas_ni_espacios_abre_sesion(self):
        respuesta = self.client.post(ENTRAR, {"correo": " ANA@ejemplo.com ", "contrasena": "clave-segura-1"})

        self.assertEqual(respuesta.status_code, 303)
        self.assertIn("_auth_user_id", self.client.session)

    def test_ac24_acceso_vuelve_a_la_ruta_local_de_origen(self):
        respuesta = self.client.post(
            f"{ENTRAR}?next=/canchas/", {"correo": "ana@ejemplo.com", "contrasena": "clave-segura-1"}
        )

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(respuesta["Location"], "/canchas/")

    def test_acceso_no_sigue_una_ruta_externa_en_next(self):
        respuesta = self.client.post(
            f"{ENTRAR}?next=https://malo.example/", {"correo": "ana@ejemplo.com", "contrasena": "clave-segura-1"}
        )

        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(respuesta["Location"], "/canchas/")

    def test_ac25_contrasena_incorrecta_se_rechaza_sin_abrir_sesion(self):
        respuesta = self.client.post(ENTRAR, {"correo": "ana@ejemplo.com", "contrasena": "otra-clave-xx"})

        self.assertEqual(respuesta.status_code, 400)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_ac25_correo_inexistente_da_el_mismo_mensaje_que_contrasena_incorrecta(self):
        con_clave_mala = self.client.post(ENTRAR, {"correo": "ana@ejemplo.com", "contrasena": "otra-clave-xx"})
        con_correo_malo = self.client.post(ENTRAR, {"correo": "nadie@ejemplo.com", "contrasena": "clave-segura-1"})

        self.assertEqual(con_correo_malo.status_code, 400)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(con_clave_mala.context["error"], con_correo_malo.context["error"])
