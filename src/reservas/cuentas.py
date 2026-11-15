"""Registro y acceso con el sistema de usuarios de Django (D-015).

El correo se guarda como `username`, sin espacios en los extremos y en minúsculas (D-014).
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

LARGO_MINIMO_CONTRASENA = 8
MENSAJE_ACCESO = "El correo o la contraseña no son correctos."


def normalizar_correo(texto):
    return (texto or "").strip().lower()


def validar_registro(nombre, correo, contrasena):
    """Devuelve un diccionario campo -> mensaje con los errores; vacío si todo es válido."""
    errores = {}
    if not (nombre or "").strip():
        errores["nombre"] = "Escribe tu nombre."
    correo_normalizado = normalizar_correo(correo)
    try:
        validate_email(correo_normalizado)
    except ValidationError:
        errores["correo"] = "Escribe un correo válido."
    else:
        if len(correo_normalizado) > 150:
            errores["correo"] = "El correo es demasiado largo."
        elif get_user_model().objects.filter(username=correo_normalizado).exists():
            errores["correo"] = "Ese correo ya tiene una cuenta."
    if len(contrasena or "") < LARGO_MINIMO_CONTRASENA:
        errores["contrasena"] = f"La contraseña debe tener al menos {LARGO_MINIMO_CONTRASENA} caracteres."
    return errores


def crear_usuario(nombre, correo, contrasena):
    return get_user_model().objects.create_user(
        username=normalizar_correo(correo), password=contrasena, first_name=nombre.strip()
    )
