# Sesión Three Amigos - Funcionalidad de Login

## Participantes
- **Product Owner**: Define los requisitos del negocio
- **Desarrollador**: Aporta perspectiva técnica
- **Tester**: Identifica casos de prueba y validaciones

## Funcionalidad: Sistema de Login

### Criterios de Aceptación

1. **Como usuario registrado**, quiero poder iniciar sesión con mi email y contraseña para acceder a mi cuenta personal.

2. **Requisitos funcionales**:
   - El email debe tener formato válido
   - La contraseña debe tener mínimo 8 caracteres
   - Máximo 3 intentos fallidos antes de bloqueo temporal (15 minutos)
   - Opción de "Recordar sesión" por 30 días
   - Mostrar mensajes de error claros

### Ejemplos Discutidos

**Escenario 1: Login exitoso**
- Usuario: juan@email.com
- Contraseña: MiClave123!
- Resultado: Redirección al dashboard

**Escenario 2: Email inválido**
- Usuario: juan@
- Contraseña: MiClave123!
- Resultado: Error "Formato de email inválido"

**Escenario 3: Contraseña incorrecta**
- Usuario: juan@email.com
- Contraseña: ClaveErronea
- Resultado: Error "Email o contraseña incorrectos"

**Escenario 4: Cuenta bloqueada**
- Después de 3 intentos fallidos
- Resultado: "Cuenta bloqueada temporalmente. Intente en 15 minutos"

### Reglas de Negocio
- El sistema no debe revelar si el email existe o no
- Los mensajes de error deben ser genéricos para evitar vulnerabilidades
- El bloqueo es por IP y email combinados
- Se debe registrar cada intento de login en logs de auditoría