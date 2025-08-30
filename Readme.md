# Sistema de Automatización de Pruebas con BDD y Performance

## Descripción del Proyecto

Este proyecto implementa un sistema completo de automatización de pruebas que incluye BDD (Behavior Driven Development), pruebas de performance, integración continua y sistema de alertas automáticas para la funcionalidad de login de una aplicación web.

## Estructura del Proyecto

```
├── features/
│   ├── login.feature              # Escenarios BDD en Gherkin
│   ├── steps/
│   │   └── login_steps.py         # Step definitions en Python
│   └── environment.py             # Configuración de entorno Behave
├── tests/
│   └── performance/
│       ├── locustfile.py          # Pruebas de performance con Locust
│       └── performance_config.py   # Configuración de umbrales
├── scripts/
│   ├── generate_report.py         # Generador de reportes HTML
│   ├── analyze_performance.py     # Analizador de métricas
│   ├── check_quality_gates.py     # Verificador de umbrales
│   └── alert_manager.py           # Gestor de alertas
├── config/
│   └── alertas.yml               # Configuración de alertas
├── .github/workflows/
│   └── bdd-pipeline.yml          # Pipeline CI/CD
├── behave.ini                    # Configuración Behave
├── requirements.txt              # Dependencias Python
└── three_amigos_session.md       # Documentación Three Amigos
```

## 1. Sesión Three Amigos

### Participantes y Roles
- **Product Owner**: Define requisitos de negocio para el sistema de login
- **Desarrollador**: Aporta perspectiva técnica de implementación
- **Tester**: Identifica casos de prueba y validaciones necesarias

### Funcionalidad Definida: Sistema de Login
Se definieron criterios de aceptación claros incluyendo validaciones de formato, límites de intentos fallidos y mensajes de error apropiados.

**Archivo**: `three_amigos_session.md`

## 2. Escenarios BDD en Gherkin

Se implementaron escenarios completos que cubren:
- Login exitoso con credenciales válidas
- Manejo de errores por contraseña incorrecta
- Validación de formato de email (Scenario Outline)
- Validación de longitud de contraseña (Scenario Outline)
- Bloqueo de cuenta después de intentos fallidos

**Archivo**: `features/login.feature`

## 3. Step Definitions en Python+Behave

### Tecnologías Utilizadas
- **Python 3.10**: Lenguaje principal
- **Behave**: Framework BDD
- **Selenium WebDriver**: Automatización de navegador
- **Page Object Model**: Patrón de diseño implementado

### Buenas Prácticas Implementadas
- Separación de responsabilidades con Page Object
- Manejo de timeouts y excepciones
- Configuración de entorno flexible (headless/visual)
- Captura automática de screenshots en fallos

**Archivos**: `features/steps/login_steps.py`, `features/environment.py`

## 4. Pipeline de Integración Continua

### Configuración del Pipeline
El pipeline incluye tres jobs principales:

1. **test-bdd**: Ejecuta pruebas BDD con reportes Allure y HTML
2. **test-performance**: Ejecuta pruebas de carga con Locust
3. **quality-gates**: Verifica umbrales de calidad y genera alertas

### Características del Pipeline
- Ejecución en Ubuntu latest
- Soporte para múltiples formatos de reporte
- Subida automática de artefactos
- Notificaciones en Pull Requests

**Archivo**: `.github/workflows/bdd-pipeline.yml`

## 5. Reportes Navegables

### Tipos de Reportes Generados
1. **Reporte HTML Behave**: Reporte básico con resultados de escenarios
2. **Reporte Allure**: Reporte interactivo con detalles completos
3. **Reporte de Calidad**: Dashboard con métricas consolidadas

### Configuración
- `behave.ini`: Configuración de formatos de salida
- `scripts/generate_report.py`: Generador de reportes personalizados

## 6. Pruebas de Performance

### Herramienta: Locust
Se implementaron dos clases de usuario:
- **LoginPerformanceTest**: Pruebas funcionales de login
- **ApiStressTest**: Pruebas de estrés del endpoint

### Indicadores Monitoreados

#### TPS (Transacciones Por Segundo)
- **Objetivo**: Mínimo 10 TPS
- **Medición**: Requests exitosos / tiempo total
- **Umbral crítico**: < 5 TPS

#### Latencia
- **P50**: Mediana de tiempos de respuesta (objetivo: < 500ms)
- **P95**: 95% de requests (objetivo: < 1500ms)
- **P99**: 99% de requests (objetivo: < 3000ms)

#### Errores
- **Tasa de error**: Porcentaje de requests fallidos
- **Umbral**: < 5% para operación normal
- **Umbral crítico**: > 10%

**Archivos**: `tests/performance/locustfile.py`, `tests/performance/performance_config.py`

## 7. Dashboard de Métricas

### Métricas Funcionales
- Tasa de éxito de pruebas BDD
- Cobertura de escenarios
- Tiempo de ejecución de suite

### Métricas de Performance
- TPS en tiempo real
- Percentiles de latencia (P50, P95, P99)
- Tasa de error por endpoint
- Usuarios concurrentes

### Visualización
Los datos se exportan en formato JSON para integración con herramientas como:
- Grafana
- Kibana
- DataDog
- New Relic

**Archivo**: `scripts/analyze_performance.py`

## 8. Sistema de Alertas Automáticas

### Canales de Notificación
- **Slack**: Alertas en tiempo real al canal #pruebas-automatizadas
- **Email**: Notificaciones críticas al equipo de QA y DevOps

### Reglas de Alertas Configuradas

#### Nivel Warning
- Latencia P95 > 1.5 segundos
- Throughput < 10 TPS

#### Nivel Critical
- Latencia P95 > 2 segundos
- Tasa de error > 5%
- Pruebas BDD con éxito < 95%

### Programación de Monitoreo
- Verificación continua cada 15 minutos
- Horario activo: 08:00-20:00 días laborables
- Reportes diarios automáticos a las 09:00

**Archivos**: `config/alertas.yml`, `scripts/alert_manager.py`

## Instalación y Ejecución

### Prerrequisitos
```bash
pip install -r requirements.txt
```

### Ejecutar Pruebas BDD
```bash
behave features/
```

### Ejecutar Pruebas de Performance
```bash
locust -f tests/performance/locustfile.py --host http://localhost:8080
```

### Generar Reportes
```bash
python scripts/generate_report.py
python scripts/analyze_performance.py
```

### Monitoreo de Alertas
```bash
python scripts/alert_manager.py
```

## Flujo Completo del Pipeline

1. **Trigger**: Push o Pull Request a main/develop
2. **Pruebas BDD**: Ejecución de escenarios con Selenium
3. **Pruebas Performance**: Carga con Locust (10 usuarios, 60s)
4. **Análisis**: Verificación de umbrales de calidad
5. **Reportes**: Generación de HTML y Allure
6. **Alertas**: Notificaciones automáticas si hay fallos
7. **Artefactos**: Subida de reportes y métricas

## Umbrales de Calidad Definidos

### Performance
- **P50**: < 500ms
- **P95**: < 1500ms  
- **P99**: < 3000ms
- **Error Rate**: < 5%
- **TPS**: > 10

### Funcionales
- **Success Rate BDD**: > 95%
- **Fallos máximos**: < 3

## Decisiones Técnicas Tomadas

### Framework BDD: Behave
**Motivo**: Integración nativa con Python, sintaxis clara en español, soporte robusto para reportes.

### Herramienta Performance: Locust  
**Motivo**: Fácil configuración, escalabilidad, reportes integrados, scripts en Python.

### Patrón Page Object
**Motivo**: Mantenibilidad del código, reutilización, separación de responsabilidades.

### Pipeline en GitHub Actions
**Motivo**: Integración nativa con repositorio, gratuito para proyectos públicos, configuración declarativa.

### Sistema de Alertas Multi-canal
**Motivo**: Notificaciones inmediatas (Slack) y formales (email) según criticidad del problema.