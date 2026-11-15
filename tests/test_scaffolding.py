from django.contrib.sessions.backends.db import SessionStore
from django.test import TestCase


class ScaffoldingTests(TestCase):
    def test_inicio_renderiza_la_plantilla_del_proyecto(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservas/inicio.html")
        self.assertContains(response, "Reservas de canchas deportivas")

    def test_sesion_se_puede_guardar_y_recuperar(self):
        session = SessionStore()
        session["origen"] = "prueba-c0"
        session.save()

        self.assertEqual(SessionStore(session_key=session.session_key)["origen"], "prueba-c0")
