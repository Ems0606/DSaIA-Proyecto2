from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe

from src.reservas import reloj, servicios
from src.reservas.dominio import ZONA_PANAMA, FechaInvalida
from src.reservas.models import Cancha


@require_safe
def inicio(request):
    return render(request, "reservas/inicio.html")


@require_safe
def catalogo(request):
    canchas = Cancha.objects.filter(activa=True)
    return render(request, "reservas/canchas.html", {"canchas": canchas})


@csrf_exempt  # Solo GET y HEAD: no escribe nada. Así require_safe responde 405 también a un POST sin token.
@require_safe
def disponibilidad(request, cancha_id):
    cancha = get_object_or_404(Cancha, pk=cancha_id, activa=True)
    ahora = reloj.ahora()
    if "fecha" in request.GET:
        texto_fecha = request.GET["fecha"]  # vacía o inválida: 400 (AC03)
    else:
        texto_fecha = ahora.astimezone(ZONA_PANAMA).date().isoformat()  # sin parámetro: hoy en Panamá
    contexto = {"cancha": cancha, "fecha_texto": texto_fecha, "franjas": []}
    try:
        fecha, franjas = servicios.consultar_disponibilidad(cancha, texto_fecha, ahora)
    except FechaInvalida as error:
        contexto["error"] = str(error)
        return render(request, "reservas/disponibilidad.html", contexto, status=400)
    contexto.update(fecha=fecha, franjas=franjas, error=None)
    return render(request, "reservas/disponibilidad.html", contexto)
