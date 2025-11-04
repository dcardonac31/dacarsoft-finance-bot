# 📊 Estructura de Google Sheets

## 🎯 Visión General

El bot crea **automáticamente** la estructura del spreadsheet cuando se ejecuta por primera vez. No necesitas crear nada manualmente.

## 📑 Hojas (Tabs) del Spreadsheet

El spreadsheet tendrá **3 hojas (pestañas)** con estructura optimizada:

```
📊 Mi Spreadsheet de Finanzas
├── 💰 Transacciones (Gastos e Ingresos UNIFICADOS)
├── 🏦 Ahorros e Inversiones (Movimientos de Capital)
└── 📘 Presupuestos
```

### ✨ **NUEVAS FUNCIONALIDADES**:

1. **Transacciones Unificadas**: Gastos e ingresos en la misma hoja con campo booleano **"Es Ingreso"**
   - `FALSE` = Gasto 💸
   - `TRUE` = Ingreso 💰

2. **Ahorros e Inversiones** 💰: Nueva hoja separada para trackear tu capital
   - Sabes DÓNDE está tu dinero
   - Seguimiento de retornos/intereses
   - Estados: activo/retirado
   - Control completo de tu patrimonio

Esto facilita enormemente el análisis y las fórmulas!

---

## 💰 Hoja: "Transacciones" (Gastos e Ingresos Unificados)

### Columnas (Headers en fila 1):

| Fecha | Monto | Categoría | Descripción | Es Ingreso |
|-------|-------|-----------|-------------|------------|
| 2025-11-04 10:30:00 | 50000 | comida | Gasté 50 mil en comida | FALSE |
| 2025-11-04 09:00:00 | 100000 | salario | Recibí 100 mil de salario | TRUE |
| 2025-11-04 14:15:00 | 15000 | transporte | Pagué en Uber | FALSE |
| 2025-11-05 16:30:00 | 250000 | freelance | Ingreso por proyecto | TRUE |
| 2025-11-04 18:45:00 | 80000 | ropa | Compré ropa | FALSE |

### ✨ Detalle de las Columnas:

1. **Fecha** (Column A)
   - Formato: `YYYY-MM-DD HH:MM:SS`
   - Ejemplo: `2025-11-04 10:30:00`
   - Tipo: Texto (se puede convertir a fecha en Sheets)

2. **Monto** (Column B)
   - Formato: Número sin formato de moneda
   - Ejemplo: `50000` (representa $50,000 COP)
   - Tipo: Número
   - ⚠️ Siempre positivo (sin signo)

3. **Categoría** (Column C)
   - Formato: Texto en minúsculas
   - Ejemplos para gastos: `comida`, `transporte`, `ropa`, `entretenimiento`
   - Ejemplos para ingresos: `salario`, `freelance`, `proyecto`, `bono`
   - Tipo: Texto

4. **Descripción** (Column D)
   - Formato: Texto libre
   - Ejemplo: `"Gasté 50 mil en comida"` o `"Recibí pago mensual"`
   - Puede estar vacío
   - Tipo: Texto

5. **Es Ingreso** (Column E) ⭐ **NUEVO - Campo Booleano**
   - Formato: Booleano (TRUE/FALSE)
   - `FALSE` = Es un GASTO 💸
   - `TRUE` = Es un INGRESO 💰
   - Tipo: Boolean
   - **Clave para filtros y análisis**

### 💡 Ventajas de la Estructura Unificada:

✅ **Fácil de analizar**: Todo en un solo lugar
✅ **Fórmulas simples**: `=SUMIF(E:E, TRUE, B:B)` para total de ingresos
✅ **Filtros directos**: Filtra por columna "Es Ingreso"
✅ **Tablas dinámicas**: Análisis más poderosos
✅ **Menos hojas**: Más organizado

---

## 🏦 Hoja: "Ahorros e Inversiones" (Movimientos de Capital)

### Columnas (Headers en fila 1):

| Fecha | Tipo | Monto | Institución | Estado | Fecha Retiro | Retorno | Descripción |
|-------|------|-------|-------------|--------|--------------|---------|-------------|
| 2025-11-04 10:00:00 | ahorro | 100000 | banco | activo | | 0 | Ahorré 100 mil en el banco |
| 2025-11-05 09:00:00 | inversion | 500000 | cdt | activo | | 0 | Invertí 500 mil en CDT |
| 2025-11-10 14:30:00 | ahorro | 200000 | davivienda | activo | | 0 | Guardé 200k en Davivienda |
| 2025-11-20 11:00:00 | inversion | 1000000 | acciones | activo | | 50000 | Inversión en acciones + retorno |

### ✨ Detalle de las Columnas:

1. **Fecha** (Column A)
   - Formato: `YYYY-MM-DD HH:MM:SS`
   - Ejemplo: `2025-11-04 10:00:00`
   - Fecha de depósito/inversión inicial
   - Tipo: Texto

2. **Tipo** (Column B)
   - Formato: `ahorro` o `inversion`
   - `ahorro` = Dinero guardado en banco, cuenta de ahorros
   - `inversion` = CDT, acciones, bonos, fondos, etc.
   - Tipo: Texto

3. **Monto** (Column C)
   - Formato: Número (capital inicial depositado)
   - Ejemplo: `100000`
   - ⚠️ Siempre positivo, sin signo
   - Tipo: Número

4. **Institución** (Column D)
   - Formato: Texto en minúsculas
   - Ejemplos: `banco`, `davivienda`, `bancolombia`, `cdt`, `acciones`, `fondos`
   - Indica DÓNDE está el dinero
   - Tipo: Texto

5. **Estado** (Column E) ⭐ **Campo clave**
   - Formato: `activo` o `retirado`
   - `activo` = El dinero está actualmente invertido/ahorrado
   - `retirado` = Ya se retiró el dinero
   - Tipo: Texto
   - **Uso**: Filtrar por "activo" para ver balance actual

6. **Fecha Retiro** (Column F)
   - Formato: `YYYY-MM-DD HH:MM:SS` o vacío
   - Ejemplo: `2025-12-01 15:00:00` o ` ` (vacío)
   - Solo se llena cuando el estado es "retirado"
   - Tipo: Texto/Fecha

7. **Retorno** (Column G)
   - Formato: Número (intereses/ganancias acumuladas)
   - Ejemplo: `50000` (ganaste $50,000)
   - Puede ser 0 si aún no hay retornos
   - Se va actualizando conforme genera intereses
   - Tipo: Número

8. **Descripción** (Column H)
   - Formato: Texto libre
   - Ejemplo: `"Ahorré 100 mil en el banco"` o `"CDT a 6 meses al 12% EA"`
   - Puede incluir notas adicionales (plazo, tasa, etc.)
   - Tipo: Texto

### 💡 Ventajas de esta Hoja:

✅ **Control de patrimonio**: Sabes EXACTAMENTE dónde está tu dinero
✅ **Tracking de retornos**: Registra ganancias de inversiones
✅ **Balance actual**: Filtra por "Estado = activo" para ver capital actual
✅ **Historial completo**: Mantiene registro de ahorros retirados
✅ **Análisis de ROI**: Calcula rendimiento (Retorno / Monto * 100)

### 📊 Fórmulas Útiles:

```excel
# Total en Ahorros ACTIVOS
=SUMIFS(C:C, B:B, "ahorro", E:E, "activo")

# Total en Inversiones ACTIVAS
=SUMIFS(C:C, B:B, "inversion", E:E, "activo")

# Total Capital ACTIVO (ahorros + inversiones)
=SUMIF(E:E, "activo", C:C)

# Total Retornos Generados
=SUM(G:G)

# Valor Actual (Capital + Retornos)
=SUMIF(E:E, "activo", C:C) + SUM(G:G)

# ROI Promedio de Inversiones
=SUM(G:G) / SUMIFS(C:C, B:B, "inversion") * 100
```

---

## 📘 Hoja: "Presupuestos"

### Columnas (Headers en fila 1):

| Fecha | Monto | Categoría | Descripción |
|-------|-------|-----------|-------------|
| 2025-11-04 08:00:00 | 300000 | transporte | Presupuesto mensual de transporte |
| 2025-11-04 08:00:00 | 1000000 | arriendo | Presupuesto mensual de arriendo |
| 2025-11-04 08:00:00 | 500000 | comida | Presupuesto mensual de comida |

### Detalle de las Columnas:

1. **Fecha** (Column A)
   - Formato: `YYYY-MM-DD HH:MM:SS`
   - Ejemplo: `2025-11-04 08:00:00`
   - Tipo: Texto

2. **Monto** (Column B)
   - Formato: Número
   - Ejemplo: `300000`
   - Tipo: Número

3. **Categoría** (Column C)
   - Formato: Texto en minúsculas
   - ⚠️ **Importante**: Debe coincidir con las categorías de gastos para comparación
   - Ejemplos: `comida`, `transporte`, `arriendo`, `entretenimiento`
   - Tipo: Texto

4. **Descripción** (Column D)
   - Formato: Texto libre
   - Ejemplo: `"Presupuesto mensual de transporte"`
   - Tipo: Texto

**Nota**: Los presupuestos NO tienen la columna "Es Ingreso" porque siempre representan límites de gasto.

---

## 🔧 Creación Automática

### ¿Qué hace el bot automáticamente?

El bot realiza estas acciones cuando se ejecuta por primera vez:

```python
# Pseudocódigo de lo que hace el bot

1. Conectar al spreadsheet
2. Verificar si existen las hojas: "Transacciones", "Presupuestos"
3. Si NO existen:
   - Crear hoja "Transacciones" con headers:
     ["Fecha", "Monto", "Categoría", "Descripción", "Es Ingreso"]
   - Crear hoja "Presupuestos" con headers:
     ["Fecha", "Monto", "Categoría", "Descripción"]
4. Si YA existen:
   - Verificar que tengan los headers correctos
   - Si no, agregar/actualizar los headers
```

### Código relevante:

En `services/sheets_service.py`:

```python
# Estructura unificada
TRANSACCIONES_SHEET = "Transacciones"
PRESUPUESTOS_SHEET = "Presupuestos"

# Headers para cada hoja
TRANSACCIONES_HEADER = ["Fecha", "Monto", "Categoría", "Descripción", "Es Ingreso"]
PRESUPUESTOS_HEADER = ["Fecha", "Monto", "Categoría", "Descripción"]
```

### Lógica de guardado:

```python
# Gastos e Ingresos → Hoja "Transacciones"
# - Campo "Es Ingreso" = FALSE para gastos
# - Campo "Es Ingreso" = TRUE para ingresos

# Presupuestos → Hoja "Presupuestos"
# - Sin campo "Es Ingreso"
```

---

## 📝 Ejemplo Visual Completo

### Cómo se ve en Google Sheets:

#### Hoja "Transacciones" (Gastos e Ingresos UNIFICADOS):
```
A                     B        C            D                          E
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1  Fecha              Monto    Categoría    Descripción                Es Ingreso
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2  2025-11-04 10:30   50000    comida       Gasté 50 mil en comida     FALSE 💸
3  2025-11-04 09:00   100000   salario      Recibí pago mensual        TRUE 💰
4  2025-11-04 14:15   15000    transporte   Pagué en Uber              FALSE 💸
5  2025-11-05 16:30   250000   freelance    Proyecto web               TRUE 💰
6  2025-11-04 18:45   80000    ropa         Compré ropa                FALSE 💸
7  2025-11-05 09:20   45000    comida       Supermercado               FALSE 💸
8  2025-11-10 11:00   500000   proyecto     Consultoría                TRUE 💰
9  2025-11-05 20:30   30000    entretenim.  Cine con amigos            FALSE 💸
```

**💡 Ventaja**: ¡Todo en una sola hoja! Fácil de filtrar, ordenar y analizar.

#### Hoja "Presupuestos":
```
A                     B        C            D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1  Fecha              Monto    Categoría    Descripción
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2  2025-11-01 08:00   300000   transporte   Presupuesto mensual
3  2025-11-01 08:00   1000000  arriendo     Presupuesto mensual
4  2025-11-01 08:00   500000   comida       Presupuesto mensual
```

---

## 🎨 Personalizaciones Opcionales

### Después de la creación automática, puedes:

#### 1. **Formatear las columnas**

En Google Sheets, puedes:
- Columna A (Fecha): Formato → Número → Fecha y hora
- Columna C (Monto): Formato → Número → Moneda
- Headers (fila 1): Negrita, fondo de color, congelar fila

#### 2. **Agregar fórmulas** ⭐ MEJORADO con la estructura unificada

Ejemplos útiles con la nueva estructura:

**Total de GASTOS (Es Ingreso = FALSE):**
```
=SUMIF(Transacciones!E:E, FALSE, Transacciones!B:B)
```

**Total de INGRESOS (Es Ingreso = TRUE):**
```
=SUMIF(Transacciones!E:E, TRUE, Transacciones!B:B)
```

**Balance (Ingresos - Gastos):**
```
=SUMIF(Transacciones!E:E, TRUE, Transacciones!B:B) - SUMIF(Transacciones!E:E, FALSE, Transacciones!B:B)
```

**Gasto Promedio:**
```
=AVERAGEIF(Transacciones!E:E, FALSE, Transacciones!B:B)
```

**Contar Gastos:**
```
=COUNTIF(Transacciones!E:E, FALSE)
```

**Contar Ingresos:**
```
=COUNTIF(Transacciones!E:E, TRUE)
```

**Gastos por Categoría (usando SUMIF):**
```
=SUMIFS(Transacciones!B:B, Transacciones!E:E, FALSE, Transacciones!C:C, "comida")
```

**Tabla Dinámica (más fácil ahora):**
- Datos → Tabla dinámica
- Filas: Categoría
- Columnas: Es Ingreso
- Valores: SUMA de Monto
- ¡Resultado: Matriz perfecta de ingresos vs gastos por categoría!

#### 3. **Crear Gráficos**

- Gráfico de pastel por categorías
- Gráfico de líneas de gastos en el tiempo
- Gráfico de barras comparando presupuesto vs gasto real

---

## 🔍 Categorías Recomendadas

### Para Gastos:
```
✅ comida
✅ transporte
✅ entretenimiento
✅ salud
✅ educación
✅ servicios (luz, agua, internet)
✅ arriendo
✅ ropa
✅ tecnología
✅ hogar
✅ deportes
✅ viajes
```

### Para Ingresos:
```
✅ salario
✅ freelance
✅ proyecto
✅ bono
✅ inversiones
✅ venta
✅ propina
```

### Para Presupuestos:
```
✅ Usar las mismas categorías que gastos
   para poder comparar presupuesto vs real
```

---

## 🚀 Proceso Completo de Uso

### 1. **Crear el Spreadsheet**
```
1. Ve a sheets.google.com
2. Crear → Nuevo spreadsheet
3. Nómbralo: "Finanzas DacarSoft"
4. Copia el ID de la URL
```

### 2. **Compartir con Service Account**
```
1. Botón "Compartir"
2. Pega el email del service account
   (está en credentials.json → client_email)
3. Dale permisos de "Editor"
4. Enviar
```

### 3. **Dejar que el bot cree la estructura**
```
1. Configura SPREADSHEET_ID en .env
2. Ejecuta: python main.py
3. El bot automáticamente:
   ✅ Crea las 3 hojas
   ✅ Agrega los headers
   ✅ ¡Listo para usar!
```

### 4. **Empezar a usar**
```
1. Envía mensajes al bot
2. Verás las transacciones aparecer automáticamente
3. Todo en tiempo real
```

---

## 🧪 Verificar la Estructura

### Script de prueba:

```bash
python test_sheets.py
```

Esto hará:
1. ✅ Conectarse al spreadsheet
2. ✅ Crear las 3 hojas si no existen
3. ✅ Agregar headers
4. ✅ Insertar 3 transacciones de prueba
5. ✅ Mostrar confirmación

### Resultado esperado:

```
✅ Connected to spreadsheet: Finanzas DacarSoft
✅ Created sheet: Gastos
✅ Created sheet: Ingresos
✅ Created sheet: Presupuestos
✅ Saved: comida - $50,000.00
✅ Saved: salario - $100,000.00
✅ Saved: transporte - $300,000.00
```

---

## 📊 Ejemplo de Análisis con la Nueva Estructura

Una vez que tengas datos, puedes crear análisis más potentes:

### Dashboard Manual en Google Sheets:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              📊 RESUMEN MENSUAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Ingresos:       $850,000  ✅ (En hoja "Transacciones", Es Ingreso = TRUE)
Total Gastos:         $520,000  💸 (En hoja "Transacciones", Es Ingreso = FALSE)
Balance:              $330,000  💰
                     
Fórmulas usadas:
Ingresos  = =SUMIF(Transacciones!E:E, TRUE, Transacciones!B:B)
Gastos    = =SUMIF(Transacciones!E:E, FALSE, Transacciones!B:B)
Balance   = Ingresos - Gastos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           💸 GASTOS POR CATEGORÍA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Comida:               $195,000  (37%)
Transporte:           $145,000  (28%)
Entretenimiento:      $90,000   (17%)
Otros:                $90,000   (18%)

Fórmula: =SUMIFS(Transacciones!B:B, Transacciones!E:E, FALSE, Transacciones!C:C, "comida")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         📊 PRESUPUESTO VS GASTO REAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Categoría      Presupuesto    Real      Diff      Estado
──────────────────────────────────────────────────────────
Comida         $200,000    $195,000   -$5,000   ✅ Dentro
Transporte     $150,000    $145,000   -$5,000   ✅ Dentro
Entretenim.    $80,000     $90,000    +$10,000  ❌ Exceso
```

### 🎯 Tabla Dinámica Recomendada

Con la estructura unificada, crea una tabla dinámica épica:

```
1. Selecciona toda la hoja "Transacciones"
2. Datos → Tabla dinámica
3. Configuración:
   - Filas: Categoría
   - Columnas: Es Ingreso
   - Valores: SUMA de Monto
   - Filtros: Fecha (para filtrar por mes)

Resultado:

Categoría      | Gasto (FALSE) | Ingreso (TRUE) | Total
───────────────|────────────---|─────────────---|───────
comida         | $195,000      | -              | $195,000
transporte     | $145,000      | -              | $145,000
salario        | -             | $100,000       | $100,000
freelance      | -             | $250,000       | $250,000
proyecto       | -             | $500,000       | $500,000
```

---

## 🔒 Seguridad de los Datos

### ✅ Buenas Prácticas:

1. **Permisos limitados**: Solo el service account tiene acceso
2. **No público**: Nunca hagas el spreadsheet público
3. **Backup**: Google Sheets tiene historial de versiones automático
4. **Acceso controlado**: Solo comparte con quien necesite

---

## 💡 Tips Avanzados

### 1. **Múltiples Spreadsheets**

Puedes tener diferentes spreadsheets para:
- Personal
- Negocio
- Familiar

Solo cambia `SPREADSHEET_ID` en `.env`

### 2. **Exportar a Excel**

```
Archivo → Descargar → Microsoft Excel (.xlsx)
```

### 3. **Apps Script para Automatizaciones**

Puedes agregar Google Apps Script para:
- Enviar reportes automáticos por email
- Crear gráficos automáticos
- Alertas de presupuesto

### 4. **Integración con Data Studio**

Conecta el spreadsheet a Google Data Studio para:
- Dashboards interactivos
- Reportes profesionales
- Compartir con otros

---

## 📚 Resumen

### ✅ Lo que DEBES hacer:

1. ✅ Crear un nuevo Google Spreadsheet
2. ✅ Compartirlo con el service account
3. ✅ Configurar SPREADSHEET_ID en .env
4. ✅ Ejecutar el bot

### ❌ Lo que NO debes hacer:

1. ❌ NO crear las hojas manualmente (el bot lo hace)
2. ❌ NO agregar headers manualmente (el bot lo hace)
3. ❌ NO cambiar los nombres de las hojas (deben ser exactos)
4. ❌ NO cambiar el orden de las columnas

### 🎯 El bot se encarga de TODO automáticamente

---

## 🆘 Problemas Comunes

### "Sheet not found"
**Solución**: Deja que el bot cree las hojas automáticamente

### "Invalid headers"
**Solución**: No modifiques los headers de la fila 1

### "Permission denied"
**Solución**: Asegúrate de compartir el spreadsheet con el service account

---

**¡Eso es todo! El bot maneja la estructura automáticamente.** 🎉

Solo necesitas:
1. Crear el spreadsheet vacío
2. Compartirlo con el service account
3. ¡El bot hace el resto!

---

*Para más información, consulta el archivo `services/sheets_service.py` donde está implementada toda la lógica.*

