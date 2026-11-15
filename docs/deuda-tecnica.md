# Deuda técnica

Lo que simplificamos a propósito para llegar a la entrega y lo que faltaría para hacerlo robusto. No se borra nada: cuando se resuelve, se marca como resuelto con la fecha.

| ID | Qué se simplificó | Qué faltaría para hacerlo robusto | Riesgo mientras tanto | Decisión |
|---|---|---|---|---|
| DT-01 | Cuentas con el modelo de usuario de Django tal cual y el correo normalizado como nombre de usuario | Modelo de usuario propio con el correo como identificador (conviene decidirlo antes de crear las migraciones de usuarios, después cuesta más), verificación de correo, recuperación de contraseña, límite de intentos de acceso y cierre de sesión | Alguien puede registrar un correo ajeno y no hay forma de recuperar la contraseña | D-015 |
| DT-02 | Interfaz con HTML y CSS planos, sin librerías externas ni calendario interactivo | Calendario visual interactivo servido desde archivos locales (sin CDN), diseño adaptable a celular y revisión de accesibilidad | La demo es sencilla y poco vistosa | D-016 |
| DT-03 | Catálogo de canchas cargado con datos de ejemplo, sin pantalla para administrarlo | Panel del encargado para dar de alta, editar y desactivar canchas y para definir horarios por cancha | Para cambiar una cancha hay que tocar los datos de ejemplo | R01 y "fuera de alcance" de `specs/outcomes.md` |
