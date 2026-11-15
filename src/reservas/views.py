from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe

from src.reservas import reloj, servicios
from src.reservas.dominio import FechaInvalida
from src.reservas.models import Cancha


@require_safe
def inicio(request):
    return render(request, "reservas/inicio.html")


@require_safe
def catalogo(request):
    canchas = Cancha.objects.filter(activa=True)
    return render(request, "reservas/canchas.html", {"canchas": canchas})


@require_safe
def disponibilidad(request, cancha_id):
    cancha = get_object_or_404(Cancha, pk=cancha_id, activa=True)
    texto_fecha = request.GET.get("fecha", "")
    contexto = {"cancha": cancha, "fecha_texto": texto_fecha, "franjas": []}
    try:
        fecha, franjas = servicios.consultar_disponibilidad(cancha, texto_fecha, reloj.ahora())
    except FechaInvalida as error:
        contexto["error"] = str(error)
        return render(request, "reservas/disponibilidad.html", contexto, status=400)
    contexto.update(fecha=fecha, franjas=franjas, error=None)
    return render(request, "reservas/disponibilidad.html", contexto)
