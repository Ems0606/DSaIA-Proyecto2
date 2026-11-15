# Arquitectura de reservas

Propuesta técnica de C0 (#3), basada en las specs v1.0 del #13. Los asuntos de producto abiertos se confirman antes de implementar sus respectivos criterios.

## Stack y capas

| Parte | Elección |
|---|---|
| Runtime | Python 3.12 |
| Web | Django 5.2, vistas, formularios, plantillas y sesiones de Django |
| Datos | SQLite, archivo local y migraciones de Django |
| Validación | `python manage.py test`, coverage.py y GitHub Actions |

Un proceso Django sirve páginas HTML y archivos estáticos locales. No hay SPA, CDN, servicio externo ni API pública. En `src/`, la configuración del proyecto conecta las URLs; las vistas y formularios validan la entrada y traducen los resultados a HTML; los servicios aplican reglas de negocio y delimitan las transacciones; la capa de modelos usa el ORM y las restricciones de SQLite. Las vistas de escritura exigen POST, sesión donde corresponda y protección CSRF. El dueño de la reserva se toma de la sesión.

## Hora civil y almacenamiento

- `USE_TZ = True` y zona de presentación `America/Panama`. El inicio y los demás instantes se guardan en UTC. Las fechas y horas introducidas se interpretan primero en Panamá y se convierten a instantes UTC conscientes de zona.
- Los servicios reciben un reloj (una función que devuelve el instante actual con zona). Para disponibilidad se calcula el intervalo semiabierto entre dos medianoches locales y se busca por esos límites en UTC. El horizonte se calcula con la **fecha local**; la antelación para cancelar se mide entre instantes. Ejemplo: 2026-11-17 21:00 en Panamá se guarda como 2026-11-18 02:00 UTC.
- Pendientes de Product: horario diario 07:00–22:00 (último inicio 21:00), duración de una hora con inicio en punto, límite inclusivo de 14 días calendario desde hoy y cancelación con al menos 2 horas. La franja a reservar debe empezar estrictamente después del instante actual. Centralizar la política de horarios en el dominio, al implementarla tras confirmar los valores.

## Exclusión de reservas simultáneas (R04, BR05)

1. Un índice único parcial de SQLite, declarado con `UniqueConstraint`, protege `(cancha, inicio)` con condición `estado = confirmada`. Consultar disponibilidad es informativo: solo la escritura en BD confirma la franja.
2. La creación y la cancelación usan transacciones cortas. Para SQLite se propone `transaction_mode = IMMEDIATE` y una espera acotada en C2, sin envolver toda la petición en una transacción. SQLite no bloquea filas con `select_for_update()`. Tras revertir una inserción fallida, solo la colisión de ese índice se traduce a `409 franja_ocupada`; otros errores de integridad conservan su tratamiento. Si SQLite agota la espera por un bloqueo, responder `503` con mensaje de reintento; el bloqueo por sí solo no demuestra que la franja esté ocupada.
3. Cancelar actualiza solo la reserva propia, confirmada y dentro del plazo; se conserva el historial, y el índice deja de incluir esa fila al confirmar el cambio. Una segunda cancelación concurrente debe ver el estado nuevo y fallar sin otro cambio.
4. AC06 se verifica con dos conexiones contra un archivo SQLite de prueba aislado, una barrera y transacciones reales: una confirmación, un conflicto y una sola fila confirmada. También se comprueban AC05 en secuencia y AC11 tras cancelar.

Referencias: [backend SQLite de Django 5.2](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes) y [restricciones del ORM](https://docs.djangoproject.com/en/5.2/ref/models/constraints/#uniqueconstraint).
