from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import OperationalError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods, require_safe

from src.reservas import cuentas, reloj, servicios
from src.reservas.dominio import ZONA_PANAMA, FechaInvalida, ReservaInvalida
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


@require_http_methods(["GET", "POST"])
def registro(request):
    if request.method == "GET":
        return render(request, "reservas/registro.html", {"datos": {}, "errores": {}})
    datos = {"nombre": request.POST.get("nombre", ""), "correo": request.POST.get("correo", "")}
    errores = cuentas.validar_registro(datos["nombre"], datos["correo"], request.POST.get("contrasena", ""))
    if errores:
        return render(request, "reservas/registro.html", {"datos": datos, "errores": errores}, status=400)
    cuentas.crear_usuario(datos["nombre"], datos["correo"], request.POST["contrasena"])
    messages.success(request, "Tu cuenta quedó creada. Ahora inicia sesión.")
    return _ver_otro(reverse("entrar"))


def _ver_otro(url):
    """Redirección 303 a un GET, como pide el contrato tras un POST válido."""
    respuesta = HttpResponse(status=303)
    respuesta["Location"] = url
    return respuesta


def _destino_seguro(request, por_defecto):
    destino = request.POST.get("next") or request.GET.get("next") or ""
    if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
        return destino
    return por_defecto


@require_http_methods(["GET", "POST"])
def entrar(request):
    siguiente = request.POST.get("next") or request.GET.get("next") or ""
    if request.method == "GET":
        return render(request, "reservas/entrar.html", {"correo": "", "error": None, "siguiente": siguiente})
    correo = cuentas.normalizar_correo(request.POST.get("correo"))
    usuario = authenticate(request, username=correo, password=request.POST.get("contrasena", ""))
    if usuario is None:
        contexto = {"correo": request.POST.get("correo", ""), "error": cuentas.MENSAJE_ACCESO, "siguiente": siguiente}
        return render(request, "reservas/entrar.html", contexto, status=400)
    login(request, usuario)
    return _ver_otro(_destino_seguro(request, reverse("canchas")))


@require_POST
def salir(request):
    logout(request)
    return _ver_otro(reverse("canchas"))


def _volver_a_disponibilidad(cancha, texto_fecha):
    return f"{reverse('disponibilidad', args=[cancha.pk])}?{urlencode({'fecha': texto_fecha})}"


@require_POST
def reservar(request, cancha_id):
    cancha = get_object_or_404(Cancha, pk=cancha_id)
    texto_fecha = request.POST.get("fecha", "")
    texto_hora = request.POST.get("hora", "")
    if not request.user.is_authenticated:
        destino = _volver_a_disponibilidad(cancha, texto_fecha)
        respuesta = HttpResponse(status=302)
        respuesta["Location"] = f"{reverse('entrar')}?{urlencode({'next': destino})}"
        return respuesta
    try:
        reserva = servicios.reservar(request.user, cancha, texto_fecha, texto_hora, reloj.ahora())
    except (FechaInvalida, ReservaInvalida) as error:
        return _rechazo(request, cancha, texto_fecha, str(error), 400)
    except servicios.CanchaInactiva:
        return _rechazo(request, cancha, texto_fecha, "Esa cancha no está disponible para reservar.", 409)
    except servicios.FranjaOcupada:
        return _rechazo(request, cancha, texto_fecha, "Esa franja ya está ocupada. Elige otra. (franja_ocupada)", 409)
    except servicios.LimiteSemanal:
        return _rechazo(
            request, cancha, texto_fecha,
            "Ya tienes dos reservas confirmadas para esa semana. Elige otra semana. (limite_semanal)",
            409,
        )
    except OperationalError:
        return _rechazo(request, cancha, texto_fecha, "El sistema está ocupado. Intenta de nuevo en unos segundos.", 503)
    messages.success(request, f"Reserva confirmada: {cancha.nombre}, {texto_fecha} a las {texto_hora}.")
    return _ver_otro(_volver_a_disponibilidad(cancha, texto_fecha))


def _rechazo(request, cancha, texto_fecha, mensaje, estado):
    """Pantalla de error de negocio; no se modificó ningún dato (BR12)."""
    contexto = {"cancha": cancha, "fecha_texto": texto_fecha, "franjas": [], "error": mensaje}
    try:
        contexto["fecha"], contexto["franjas"] = servicios.consultar_disponibilidad(cancha, texto_fecha, reloj.ahora())
    except FechaInvalida:
        pass
    return render(request, "reservas/disponibilidad.html", contexto, status=estado)
