# Ajuste de C2 tras la revisión de #19 (2026-11-15)

Rey sugirió que `servicios.reservar` no traduzca cualquier `IntegrityError` a `franja_ocupada`, porque la arquitectura pide traducir solo la colisión de `reserva_confirmada_unica`. Hoy no hay otra restricción que pueda dispararse al crear una reserva, pero el día que exista, el error se habría disfrazado de franja ocupada.

**Cambio:** tras un `IntegrityError` se vuelve a comprobar si ya hay una reserva confirmada en esa cancha e inicio. Si la hay, es la colisión de la franja y responde `FranjaOcupada`. Si no, el error se propaga. No se lee el texto del error porque en SQLite no incluye el nombre del índice parcial.

**Pruebas nuevas** (`tests/test_c2_integridad.py`):
- `test_r04_otro_error_de_integridad_no_se_traduce_a_franja_ocupada`
- `test_r04_si_otra_solicitud_ocupo_la_franja_se_traduce_a_franja_ocupada`

| Paso | Resultado real |
|---|---|
| En rojo, antes del cambio | 2 errores: la primera lanza `FranjaOcupada` en vez de propagar el error; la segunda falla porque aún no existe el auxiliar `_hay_confirmada` |
| En verde, después del cambio | 65 pruebas OK (63 anteriores y 2 nuevas), cobertura 96 %, concurrencia 20 de 20 |
