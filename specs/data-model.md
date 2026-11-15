# Modelo de datos

Propuesta de C0 (#3). Las tablas del dominio se agregan en los ciclos indicados.

| Entidad | Campos y restricciones | Ciclo |
|---|---|---|
| Cancha | ID, nombre y deporte no vacíos, activa (booleano). Carga repetible de canchas ficticias para la demo. | C1 |
| Usuario | ID, nombre visible, correo único y contraseña con hash de Django; el correo se usa para iniciar sesión si Product confirma el supuesto de cuentas. | C2 |
| Reserva | ID, FK a Cancha, FK a Usuario, inicio UTC, estado (confirmada/cancelada), creada en UTC y cancelada en UTC (nulo mientras esté confirmada). | C2; transición en C4 |

- Una cancha y un usuario pueden tener muchas reservas. Usar `PROTECT` para conservar el historial y `settings.AUTH_USER_MODEL` para la relación con el usuario.
- No hay una tabla de franjas: se generan para la fecha civil a partir de la política de horarios. La franja se identifica por cancha e inicio, y el final se deriva de la duración fija de v1.0. Si se admite cambiar la duración para reservas ya creadas, se deberá revisar cómo conservar el final acordado.
- `UniqueConstraint(fields=["cancha", "inicio"], condition=Q(estado="confirmada"), name="reserva_confirmada_unica")`. Los campos de esa clave y el estado son obligatorios. Una restricción de comprobación admite solo confirmada con cancelación nula o cancelada con instante de cancelación. Índices de consulta: `(cancha, inicio)` para disponibilidad e `(usuario, inicio)` para el historial.
- Si se confirma el acceso por correo, crear un modelo de usuario de Django en la migración inicial de su app, antes de migrar reservas y antes de tener datos de usuarios. Propuesta pendiente de Product: recortar espacios y tratar mayúsculas como equivalentes para el correo tanto al registrar como al iniciar sesión; guardar el valor canónico con unicidad en BD. Usar los hashers de Django. Las BD locales de C0/C1 son de prueba; verificar las migraciones desde cero en C2 antes de continuar.
- v1.0 no impone cupo semanal (BR10, AC20). No se agrega un campo de contador ni se anticipan restricciones de v1.1.
