from django.core.management.base import BaseCommand

from src.reservas.models import Cancha

CANCHAS_DEMO = [
    {"nombre": "Cancha 1", "deporte": "Fútbol 5"},
]


class Command(BaseCommand):
    help = "Carga las canchas ficticias de la demo. Es repetible: no duplica canchas."

    def handle(self, *args, **options):
        for datos in CANCHAS_DEMO:
            cancha, creada = Cancha.objects.get_or_create(
                nombre=datos["nombre"],
                defaults={"deporte": datos["deporte"], "activa": True},
            )
            estado = "creada" if creada else "ya existía"
            self.stdout.write(f"{cancha.nombre}: {estado}")
