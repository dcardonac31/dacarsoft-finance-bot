# 📝 Changelog

Todos los cambios importantes del proyecto serán documentados en este archivo.

---

## [1.2.0] - 2025-11-04

### ✨ NUEVO: Ahorros e Inversiones (Propuesta 2 Implementada)

#### Cambios Principales

**Nueva hoja "Ahorros e Inversiones"** para tracking de capital (separado de flujo operativo)

**Estructura actual:**
- 3 hojas: Transacciones, **Ahorros e Inversiones**, Presupuestos
- Ahorros e Inversiones: Fecha, Tipo, Monto, Institución, Estado, Fecha Retiro, Retorno, Descripción

#### Beneficios

✅ **Separación conceptual**
- Transacciones = Flujo operativo (gastos/ingresos diarios)
- Ahorros e Inversiones = Movimientos de capital
- Presupuestos = Planificación

✅ **Tracking de patrimonio**
- Sabes DÓNDE está tu dinero (banco, CDT, acciones, etc.)
- Estados: activo/retirado
- Seguimiento de retornos e intereses

✅ **Análisis completo**
- Balance operativo vs balance patrimonial
- ROI de inversiones
- Capital activo en tiempo real

#### Nuevas Funcionalidades

**Parser LLM actualizado:**
- Reconoce mensajes de ahorros e inversiones
- Palabras clave: "ahorré", "guardé", "invertí", "CDT", "acciones"
- Diferencia automáticamente operativo vs capital

**Ejemplos de uso:**
```
"Ahorré 100 mil en el banco"     → Hoja: Ahorros e Inversiones
"Invertí 500 mil en CDT"         → Hoja: Ahorros e Inversiones
"Gasté 50 mil en comida"         → Hoja: Transacciones
"Recibí 100 mil de salario"      → Hoja: Transacciones
```

#### Archivos Nuevos

- `domain/capital.py` (NUEVO)
  - ✅ Modelo `CapitalMovement` con validación Pydantic
  - ✅ Enums: `CapitalType` (ahorro/inversion), `CapitalStatus` (activo/retirado)
  - ✅ Métodos: `get_current_value()`, `is_active()`, `withdraw()`, `add_return()`

#### Archivos Modificados

- `domain/transaction.py`
  - ✅ Agregados tipos: `AHORRO`, `INVERSION` a `TransactionType`

- `domain/__init__.py`
  - ✅ Exporta `CapitalMovement`, `CapitalType`, `CapitalStatus`

- `services/sheets_service.py`
  - ✅ Nueva constante: `CAPITAL_SHEET = "Ahorros e Inversiones"`
  - ✅ Nuevo header: `CAPITAL_HEADER` (8 columnas)
  - ✅ Método nuevo: `save_capital_movement()`
  - ✅ Método nuevo: `get_capital_movements(only_active)`
  - ✅ `initialize_sheets()` ahora crea 3 hojas

- `services/llm_service.py`
  - ✅ System prompt actualizado para reconocer ahorros e inversiones
  - ✅ `parse_message()` ahora retorna tupla: `(object, "transaction"|"capital")`
  - ✅ Distingue automáticamente tipo de mensaje
  - ✅ Palabras clave agregadas para clasificación

- `bot/handlers.py`
  - ✅ `handle_message()` maneja ambos tipos (transaction/capital)
  - ✅ Mensajes diferentes según tipo
  - ✅ Emojis: 🏦 para ahorros, 📈 para inversiones
  - ✅ `help_command()` incluye ejemplos de ahorros/inversiones

- `README.md`
  - ✅ Actualizada estructura de sheets (ahora 3 hojas)
  - ✅ Beneficios de la separación operativo/capital
  - ✅ Ejemplos de ahorros e inversiones

- `SHEETS_STRUCTURE.md`
  - ✅ Sección completa para "Ahorros e Inversiones"
  - ✅ Detalle de las 8 columnas
  - ✅ Fórmulas útiles para análisis de capital
  - ✅ Ejemplos de cálculo de ROI

#### Retrocompatibilidad

✅ **Compatible**: Los datos existentes en "Transacciones" y "Presupuestos" no se ven afectados.
✅ **Actualización automática**: El bot crea la nueva hoja "Ahorros e Inversiones" automáticamente.

---

## [1.1.0] - 2025-11-04

### ✨ NUEVO: Estructura Unificada de Gastos e Ingresos

#### Cambios Principales

**Antes:**
- 3 hojas separadas: Gastos, Ingresos, Presupuestos
- Columnas: Fecha, Tipo, Monto, Categoría, Descripción

**Ahora:**
- 2 hojas optimizadas: Transacciones (unificada), Presupuestos
- Transacciones: Fecha, Monto, Categoría, Descripción, **Es Ingreso** (booleano)
- Presupuestos: Fecha, Monto, Categoría, Descripción

#### Beneficios

✅ **Análisis más simple**
- Fórmula para total gastos: `=SUMIF(E:E, FALSE, B:B)`
- Fórmula para total ingresos: `=SUMIF(E:E, TRUE, B:B)`
- Balance en una sola fórmula

✅ **Tablas dinámicas más poderosas**
- Una tabla con filas (Categoría) y columnas (Es Ingreso)
- Ver gastos vs ingresos por categoría automáticamente

✅ **Filtros más eficientes**
- Filtrar por "Es Ingreso" = TRUE para ver solo ingresos
- Filtrar por "Es Ingreso" = FALSE para ver solo gastos

✅ **Mejor organización**
- De 3 hojas a 2 hojas
- Todo relacionado con transacciones en un solo lugar

#### Archivos Modificados

- `domain/transaction.py`
  - ✅ Agregado método `is_income()` 
  - ✅ Actualizado `to_sheets_row()` para nueva estructura

- `services/sheets_service.py`
  - ✅ Cambiado de `SHEET_NAMES` dict a constantes `TRANSACCIONES_SHEET` y `PRESUPUESTOS_SHEET`
  - ✅ Nuevos headers: `TRANSACCIONES_HEADER` y `PRESUPUESTOS_HEADER`
  - ✅ Actualizado `initialize_sheets()` para crear solo 2 hojas
  - ✅ Actualizado `save_transaction()` para guardar en hoja correcta con estructura correcta
  - ✅ Actualizado `get_transactions()` para filtrar por campo booleano

- `SHEETS_STRUCTURE.md`
  - ✅ Actualizada toda la documentación con nueva estructura
  - ✅ Ejemplos de fórmulas mejoradas
  - ✅ Casos de uso con campo booleano

- `SHEETS_STRUCTURE_COMPARISON.md` (NUEVO)
  - ✅ Comparación detallada antes vs después
  - ✅ Ejemplos de migración
  - ✅ Beneficios explicados

- `README.md`
  - ✅ Actualizada sección de estructura de Google Sheets

#### Retrocompatibilidad

⚠️ **Cambio Breaking**: Si tienes un spreadsheet existente con la estructura antigua, el bot creará las nuevas hojas automáticamente. Los datos antiguos NO se migran automáticamente.

**Para migrar datos antiguos:**
Ver archivo `SHEETS_STRUCTURE_COMPARISON.md` sección "Ejemplo Real de Migración"

---

## [1.0.0] - 2025-11-04

### 🎉 Versión Inicial

#### Características Implementadas

- ✅ Bot de Telegram funcional
- ✅ Comandos: /start, /help, /stats
- ✅ Procesamiento de lenguaje natural con OpenAI GPT
- ✅ Integración con Google Sheets
- ✅ Validación con Pydantic
- ✅ Arquitectura limpia (domain, services, bot)
- ✅ FastAPI integration
- ✅ Modo standalone
- ✅ Documentación completa
- ✅ Scripts de testing

#### Módulos

**Bot Layer**
- `bot/handlers.py` - Manejadores de comandos y mensajes
- `bot/bot_instance.py` - Instancia del bot

**Domain Layer**
- `domain/transaction.py` - Modelo Transaction con validación

**Services Layer**
- `services/config.py` - Gestión de configuración
- `services/llm_service.py` - Integración OpenAI
- `services/sheets_service.py` - Integración Google Sheets

**Application Layer**
- `main.py` - Entry point con FastAPI

#### Documentación

- `README.md` - Documentación principal
- `QUICKSTART.md` - Guía rápida
- `setup_guide.md` - Setup detallado
- `DEPLOYMENT.md` - Guías de deployment
- `CONTRIBUTING.md` - Guía de contribución
- `PROJECT_SUMMARY.md` - Resumen técnico
- `SHEETS_STRUCTURE.md` - Estructura de sheets
- `services/README.md` - Documentación de servicios

#### Scripts

- `test_llm.py` - Prueba del servicio LLM
- `test_sheets.py` - Prueba de Google Sheets
- `run_bot.bat` - Launcher para Windows
- `run_bot.sh` - Launcher para Linux/Mac

---

## Formato de Versionado

Este proyecto sigue [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles de API
- **MINOR**: Nueva funcionalidad compatible
- **PATCH**: Correcciones de bugs

---

## Tipos de Cambios

- **✨ Agregado**: Para nuevas funcionalidades
- **🔧 Cambiado**: Para cambios en funcionalidad existente
- **⚠️ Deprecado**: Para funcionalidades que serán removidas
- **🗑️ Removido**: Para funcionalidades removidas
- **🐛 Corregido**: Para corrección de bugs
- **🔒 Seguridad**: Para vulnerabilidades

---

*Para ver la versión actual: `git describe --tags`*
*Para ver todos los cambios: `git log --oneline`*

