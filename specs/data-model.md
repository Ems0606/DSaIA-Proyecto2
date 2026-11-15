# Modelo de datos

Propuesta de C0 (#3). Las tablas del dominio se agregan en los ciclos indicados.

| Entidad | Campos y restricciones | Ciclo |
|---|---|---|
| Cancha | ID, nombre y deporte no vacíos, activa (booleano). Carga repetible de canchas ficticias para la demo. | C1 |
| Usuario de Django (`auth.User`) | ID, `first_name` para el nombre visible, `username` único que guarda el correo normalizado y `password` con hash de Django. | Tabla disponible desde C0; registro y acceso en C2 |
| Reserva | ID, FK a Cancha, FK a Usuario, inicio UTC, estado (confirmada/cancelada), creada en UTC y cancelada en UTC (nulo mientras esté confirmada). | C2; transición en C4 |

- Una cancha y un usuario pueden tener muchas reservas. Usar `PROTECT` para conservar el historial y `settings.AUTH_USER_MODEL` para la relación con el usuario.
- No hay una tabla de franjas: se generan para la fecha civil a partir de la política de horarios. La franja se identifica por cancha e inicio, y el final se deriva de la duración fija de v1.0. Si se admite cambiar la duración para reservas ya creadas, se deberá revisar cómo conservar el final acordado.
- `UniqueConstraint(fields=["cancha", "inicio"], condition=Q(estado="confirmada"), name="reserva_confirmada_unica")`. Los campos de esa clave y el estado son obligatorios. Una restricción de comprobación admite solo confirmada con cancelación nula o cancelada con instante de cancelación. Índices de consulta: `(cancha, inicio)` para disponibilidad e `(usuario, inicio)` para el historial.
- D-014 y D-015 fijan la misma normalización al registrar y al iniciar sesión: recortar espacios en los extremos y convertir a minúsculas. Validar el formato y la longitud antes de persistir: `auth.User.username` admite hasta 150 caracteres. Usar su unicidad en BD y el gestor de usuarios de Django para guardar la contraseña con hash. El identificador de acceso es `username`. El modelo propio, la verificación de correo y la recuperación de contraseña se registran en [DT-01](../docs/deuda-tecnica.md).
- v1.0 no impone cupo semanal (BR10, AC20). No se agrega un campo de contador ni se anticipan restricciones de v1.1.
