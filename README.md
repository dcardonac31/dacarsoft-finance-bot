# 🤖 Dacarsoft Asistente Financiero Bot

Un bot de Telegram inteligente para rastrear finanzas personales usando lenguaje natural. Proyecto educativo del canal de YouTube **DacarSoft**.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Características

- 💬 **Lenguaje Natural**: Envía mensajes como "Gasté 50 mil en comida" y el bot los interpreta automáticamente
- 🧠 **Inteligencia Artificial**: Usa OpenAI GPT para analizar mensajes en español
- 📊 **Google Sheets**: Persiste datos automáticamente en Google Sheets
- 🏗️ **Arquitectura Limpia**: Código bien estructurado y documentado para aprendizaje
- ⚡ **FastAPI Integration**: API REST opcional para extender funcionalidad
- 🔐 **Seguro**: Gestión de credenciales mediante variables de entorno

## 🎯 Tipos de Transacciones

El bot puede registrar tres tipos de operaciones:

### 💸 Gastos
```
"Gasté 50 mil en comida"
"Pagué 15000 en Uber"
"Compré ropa por 80 mil"
```

### 💰 Ingresos
```
"Recibí 100 mil de salario"
"Ingreso de 250k por freelance"
```

### 📊 Presupuestos
```
"Presupuesto de 300 mil para transporte"
"Presupuesto mensual de 1 millón para arriendo"
```

## 🏗️ Arquitectura

```
dacarsoft-finance-bot/
├── bot/                      # Telegram bot handlers
│   ├── __init__.py
│   ├── bot_instance.py       # Bot application instance
│   └── handlers.py           # Command and message handlers
├── services/                 # External integrations
│   ├── __init__.py
│   ├── config.py             # Configuration management
│   ├── llm_service.py        # OpenAI integration
│   └── sheets_service.py     # Google Sheets integration
├── domain/                   # Business entities
│   ├── __init__.py
│   └── transaction.py        # Transaction model
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (create this)
```

## 🚀 Instalación

### 1. Requisitos Previos

- Python 3.11 o superior
- Cuenta de Telegram
- Cuenta de Google Cloud (para Google Sheets API)
- Cuenta de OpenAI (para GPT API)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/dacarsoft/dacarsoft-finance-bot.git
cd dacarsoft-finance-bot
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar el Bot de Telegram

1. Habla con [@BotFather](https://t.me/BotFather) en Telegram
2. Crea un nuevo bot con `/newbot`
3. Sigue las instrucciones y copia el token que te da
4. Guarda el token para el siguiente paso

### 6. Configurar Google Sheets

#### Crear Proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita las siguientes APIs:
   - Google Sheets API
   - Google Drive API

#### Crear Credenciales

1. Ve a "APIs & Services" > "Credentials"
2. Crea una "Service Account"
3. Genera una clave JSON para la cuenta de servicio
4. Descarga el archivo JSON y guárdalo como `services/credentials.json`

#### Crear y Compartir Spreadsheet

1. Crea un nuevo Google Spreadsheet
2. Copia el ID del spreadsheet (está en la URL)
   ```
   https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
   ```
3. Comparte el spreadsheet con el email de tu service account
   - Abre el archivo JSON de credenciales
   - Busca el campo `client_email`
   - Comparte el spreadsheet con ese email (con permisos de edición)

### 7. Configurar OpenAI

1. Ve a [OpenAI Platform](https://platform.openai.com/)
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys"
4. Crea una nueva API key
5. Copia la clave para el siguiente paso

### 8. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Telegram Bot Configuration
BOT_NAME="Dacarsoft Asistente Financiero Bot"
BOT_USERNAME="DacarsoftFinanceBot"
BOT_TOKEN="tu_token_de_telegram_aqui"

# Google Sheets Configuration
SHEETS_CREDENTIALS_FILE="services/credentials.json"
SPREADSHEET_ID="tu_spreadsheet_id_aqui"

# OpenAI Configuration
OPENAI_API_KEY="tu_openai_api_key_aqui"

# FastAPI Configuration
API_HOST="0.0.0.0"
API_PORT=8000

# Application Configuration
TIMEZONE="America/Bogota"
DEBUG=True
```

## ▶️ Ejecución

### Modo con FastAPI (Recomendado)

Incluye el bot de Telegram + API REST:

```bash
python main.py
```

El bot estará corriendo y además tendrás acceso a:
- API REST: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Modo Standalone (Solo Bot)

Si solo necesitas el bot sin API:

```bash
python main.py --standalone
```

## 📝 Uso del Bot

1. Busca tu bot en Telegram por el username configurado
2. Envía `/start` para comenzar
3. Envía mensajes en lenguaje natural:
   - "Gasté 50 mil en comida"
   - "Recibí 100 mil de salario"
   - "Presupuesto de 300 mil para transporte"

### Comandos Disponibles

- `/start` - Iniciar el bot y ver mensaje de bienvenida
- `/help` - Ver ayuda y ejemplos de uso
- `/stats` - Ver estadísticas (próximamente)

## 🧪 Estructura de Datos

### Formato JSON de Transacciones

```json
{
  "tipo": "gasto",
  "monto": 50000,
  "categoria": "comida",
  "descripcion": "Gasté 50 mil en comida",
  "fecha": "2025-11-04T10:30:00"
}
```

### Estructura en Google Sheets ⭐ NUEVA CON AHORROS E INVERSIONES

El bot crea automáticamente TRES hojas con estructura optimizada:

1. **Transacciones**: Gastos E Ingresos UNIFICADOS (operativos)
   - Columnas: Fecha, Monto, Categoría, Descripción, **Es Ingreso** (TRUE/FALSE)
   - ✅ Ventaja: Todo en un solo lugar, fácil de analizar

2. **Ahorros e Inversiones**: Movimientos de capital 💰
   - Columnas: Fecha, Tipo, Monto, Institución, Estado, Fecha Retiro, Retorno, Descripción
   - ✅ Trackea DÓNDE está tu dinero y cuánto has ganado

3. **Presupuestos**: Todos los presupuestos definidos
   - Columnas: Fecha, Monto, Categoría, Descripción

**Beneficios de la estructura:**
- ✅ Separación clara: flujo operativo vs capital
- ✅ Fórmulas más simples: `=SUMIF(E:E, TRUE, B:B)` para ingresos
- ✅ Tracking completo de patrimonio
- ✅ Seguimiento de retornos de inversiones
- ✅ Estados activo/retirado para balance actual

## 🔧 Desarrollo

### Estructura del Código

#### `domain/transaction.py`
Modelo de datos Pydantic con validación para transacciones financieras.

#### `services/config.py`
Gestión centralizada de configuración usando Pydantic Settings.

#### `services/llm_service.py`
Servicio para interpretar mensajes en lenguaje natural usando OpenAI GPT.

#### `services/sheets_service.py`
Integración con Google Sheets API para persistencia de datos.

#### `bot/handlers.py`
Manejadores de comandos y mensajes del bot de Telegram.

#### `main.py`
Punto de entrada principal con soporte para FastAPI y modo standalone.

### Agregar Nuevas Funcionalidades

#### 1. Nuevo Comando

Edita `bot/handlers.py`:

```python
async def mi_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mi respuesta")

# En setup_handlers:
application.add_handler(CommandHandler("micomando", mi_comando))
```

#### 2. Nueva Categoría

El sistema reconoce automáticamente categorías, pero puedes agregar lógica personalizada en `services/llm_service.py`.

#### 3. Nuevos Endpoints API

Edita `main.py`:

```python
@app.get("/mi-endpoint")
async def mi_endpoint():
    return {"mensaje": "Hola"}
```

## 🐛 Solución de Problemas

### Error: "No module named 'telegram'"

```bash
pip install python-telegram-bot --upgrade
```

### Error: Google Sheets Authentication Failed

1. Verifica que `services/credentials.json` existe
2. Verifica que el spreadsheet está compartido con el service account
3. Revisa que las APIs están habilitadas en Google Cloud

### Error: OpenAI API Key Invalid

1. Verifica que la API key es correcta
2. Asegúrate de tener créditos en tu cuenta de OpenAI
3. Verifica que la key tiene permisos para usar GPT-4

### Bot no responde

1. Verifica que el token del bot es correcto
2. Revisa los logs en la consola
3. Asegúrate que el bot no está bloqueado por el usuario

## 📚 Recursos Educativos

Este proyecto es ideal para aprender sobre:

- **Python async/await**: Todo el código usa programación asíncrona moderna
- **Clean Architecture**: Separación clara de capas (domain, services, bot)
- **Telegram Bots**: Implementación completa con python-telegram-bot
- **Google APIs**: Integración con Google Sheets API
- **OpenAI GPT**: Uso de LLMs para procesamiento de lenguaje natural
- **FastAPI**: Creación de APIs REST modernas
- **Pydantic**: Validación de datos con type hints

## 🚀 Deployment

### Render.com

1. Crea una cuenta en [Render](https://render.com)
2. Conecta tu repositorio de GitHub
3. Crea un nuevo "Web Service"
4. Configura las variables de entorno
5. Deploy automático

### Replit

1. Importa el proyecto desde GitHub
2. Configura los Secrets (variables de entorno)
3. Ejecuta `python main.py`

### Railway

1. Conecta tu repositorio
2. Configura variables de entorno
3. Deploy automático

## 📹 Videos del Canal DacarSoft

Este proyecto fue desarrollado como parte de una serie educativa. Visita el canal de YouTube [DacarSoft](https://youtube.com/@DacarSoft) para:

- Tutoriales paso a paso
- Explicación de la arquitectura
- Mejores prácticas de Python
- Integración con APIs externas

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

## 👨‍💻 Autor

**David Sneider Cardona Cardenas**
- YouTube: [@DacarSoft](https://youtube.com/@DacarSoft)
- GitHub: [@dacarsoft](https://github.com/dacarsoft)

## 🙏 Agradecimientos

- Comunidad de Python
- python-telegram-bot developers
- OpenAI team
- Google Cloud Platform
- Todos los suscriptores de DacarSoft

---

⭐ Si este proyecto te fue útil, no olvides darle una estrella en GitHub!

📺 Suscríbete al canal de YouTube [DacarSoft](https://youtube.com/@DacarSoft) para más contenido educativo!
