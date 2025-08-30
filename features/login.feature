# language: es

Característica: Sistema de Login
  Como usuario de la plataforma
  Quiero poder iniciar sesión de forma segura
  Para acceder a mi cuenta personal

  Antecedentes:
    Dado que estoy en la página de login

  Escenario: Login exitoso con credenciales válidas
    Cuando ingreso el email "usuario@ejemplo.com"
    Y ingreso la contraseña "ContraseñaSegura123!"
    Y hago clic en el botón iniciar sesión
    Entonces debería ser redirigido al dashboard
    Y debería ver el mensaje "Bienvenido"

  Escenario: Login fallido con contraseña incorrecta
    Cuando ingreso el email "usuario@ejemplo.com"
    Y ingreso la contraseña "ContraseñaIncorrecta"
    Y hago clic en el botón iniciar sesión
    Entonces debería permanecer en la página de login
    Y debería ver el mensaje de error "Email o contraseña incorrectos"

  Esquema del escenario: Validación de formato de email
    Cuando ingreso el email "<email>"
    Y ingreso la contraseña "ContraseñaValida123!"
    Y hago clic en el botón iniciar sesión
    Entonces debería ver el mensaje de error "<mensaje_error>"

    Ejemplos:
      | email              | mensaje_error                |
      | usuario@           | Formato de email inválido   |
      | @ejemplo.com       | Formato de email inválido   |
      | usuario.com        | Formato de email inválido   |
      | usuario@ejemplo    | Formato de email inválido   |

  Esquema del escenario: Validación de longitud de contraseña
    Cuando ingreso el email "usuario@ejemplo.com"
    Y ingreso la contraseña "<contraseña>"
    Y hago clic en el botón iniciar sesión
    Entonces debería ver el mensaje de error "<mensaje_error>"

    Ejemplos:
      | contraseña | mensaje_error                            |
      | abc123     | La contraseña debe tener mínimo 8 caracteres |
      | 1234567    | La contraseña debe tener mínimo 8 caracteres |
      | test       | La contraseña debe tener mínimo 8 caracteres |

  Escenario: Bloqueo de cuenta después de intentos fallidos
    Cuando intento iniciar sesión 3 veces con credenciales incorrectas
    Entonces mi cuenta debería estar bloqueada temporalmente
    Y debería ver el mensaje "Cuenta bloqueada temporalmente. Intente en 15 minutos"