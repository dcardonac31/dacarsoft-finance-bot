# ⚡ Quick Start Guide

¿Quieres empezar rápido? Esta guía te llevará de 0 a bot funcionando en ~30 minutos.

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener:

- ✅ Python 3.11+ instalado
- ✅ Cuenta de Telegram
- ✅ 30 minutos de tiempo

## 🚀 Instalación en 5 Pasos

### 1️⃣ Clonar e Instalar (2 minutos)

```bash
# Clonar el repositorio
git clone https://github.com/dacarsoft/dacarsoft-finance-bot.git
cd dacarsoft-finance-bot

# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Crear Bot en Telegram (3 minutos)

1. Abre Telegram y busca **@BotFather**
2. Envía `/newbot`
3. Dale un nombre: `Tu Finance Bot`
4. Dale un username: `TuFinanceBot` (debe terminar en "bot")
5. **Copia el token** que te da (lo usarás en el paso 4)

### 3️⃣ Configurar Google Sheets (10 minutos)

#### A. Crear Proyecto en Google Cloud

1. Ve a: https://console.cloud.google.com/
2. Crea un nuevo proyecto: "Finance Bot"
3. Habilita estas APIs:
   - Google Sheets API ✓
   - Google Drive API ✓

#### B. Crear Service Account

1. Ve a: APIs & Services → Credentials
2. Create Credentials → Service Account
3. Nombre: `finance-bot-service`
4. Role: Editor
5. Create and Continue → Done

#### C. Descargar Credenciales

1. Clic en el service account creado
2. Keys → Add Key → Create new key
3. Tipo: JSON
4. Se descargará un archivo
5. **Guárdalo como** `services/credentials.json` en tu proyecto

#### D. Crear Spreadsheet

1. Ve a: https://sheets.google.com
2. Crea nuevo spreadsheet: "Mis Finanzas"
3. Copia el ID de la URL:
   ```
   https://docs.google.com/spreadsheets/d/[COPIA_ESTE_ID]/edit
   ```
4. Comparte el sheet con el email del service account:
   - Abre `services/credentials.json`
   - Busca `"client_email"`
   - Comparte el sheet con ese email (permisos de Editor)

### 4️⃣ Configurar OpenAI (5 minutos)

1. Ve a: https://platform.openai.com/
2. Crea cuenta / Inicia sesión
3. Ve a: API Keys
4. Create new secret key
5. **Copia la key** (solo la verás una vez)
6. Agrega $5-10 de crédito a tu cuenta

### 5️⃣ Configurar Variables de Entorno (5 minutos)

Crea un archivo `.env` en la raíz del proyecto:

```env
BOT_TOKEN="PEGA_AQUI_TOKEN_DE_BOTFATHER"
SPREADSHEET_ID="PEGA_AQUI_ID_DEL_SPREADSHEET"
OPENAI_API_KEY="PEGA_AQUI_KEY_DE_OPENAI"

# Las siguientes ya están OK por defecto
BOT_NAME="Dacarsoft Asistente Financiero Bot"
BOT_USERNAME="DacarsoftFinanceBot"
SHEETS_CREDENTIALS_FILE="services/credentials.json"
API_HOST="0.0.0.0"
API_PORT=8000
TIMEZONE="America/Bogota"
DEBUG=True
```

**Reemplaza** los valores marcados con "PEGA_AQUI" con tus propios valores.

## ▶️ Ejecutar el Bot (5 minutos)

### En Windows:

```bash
# Opción 1: Usar el script
run_bot.bat

# Opción 2: Manual
venv\Scripts\activate
python main.py
```

### En Linux/Mac:

```bash
# Opción 1: Usar el script
chmod +x run_bot.sh
./run_bot.sh

# Opción 2: Manual
source venv/bin/activate
python main.py
```

Deberías ver:

```
INFO - Starting Dacarsoft Finance Bot...
INFO - Successfully authenticated with Google Sheets
INFO - Connected to spreadsheet: Mis Finanzas
INFO - Created sheet: Gastos
INFO - Created sheet: Ingresos
INFO - Created sheet: Presupuestos
INFO - Bot started: @TuFinanceBot
INFO - Uvicorn running on http://0.0.0.0:8000
```

## ✅ Probar el Bot

1. Abre Telegram
2. Busca tu bot (el username que configuraste)
3. Envía: `/start`
4. Deberías recibir un mensaje de bienvenida
5. Prueba: `Gasté 50 mil en comida`
6. El bot procesará y responderá
7. ¡Verifica tu Google Spreadsheet! 📊

## 🎉 ¡Listo!

Tu bot está funcionando. Ahora puedes:

- 💬 Enviar mensajes como: "Gasté 30 mil en transporte"
- 💰 Registrar ingresos: "Recibí 200 mil de salario"
- 📊 Definir presupuestos: "Presupuesto de 100 mil para comida"
- 📈 Ver todo en tiempo real en Google Sheets

## 🧪 Scripts de Prueba

Antes de usar el bot, puedes probar los componentes:

```bash
# Probar OpenAI parsing
python test_llm.py

# Probar Google Sheets
python test_sheets.py
```

## 🆘 Problemas Comunes

### ❌ "No module named 'telegram'"

```bash
pip install python-telegram-bot --upgrade
```

### ❌ "Google Sheets authentication failed"

1. ¿Existe `services/credentials.json`?
2. ¿Compartiste el sheet con el service account?
3. ¿Habilitaste las APIs en Google Cloud?

### ❌ "OpenAI API error"

1. ¿La API key es correcta?
2. ¿Tienes créditos en tu cuenta?
3. Verifica en: https://platform.openai.com/account/usage

### ❌ "Bot not responding"

1. ¿El BOT_TOKEN es correcto?
2. ¿El bot está corriendo? (checa la consola)
3. ¿Bloqueaste al bot en Telegram? (desbloquealo)

## 📚 Siguiente Pasos

Ahora que tu bot funciona:

1. **Personaliza**: Edita mensajes en `bot/handlers.py`
2. **Aprende**: Lee el código en `domain/` y `services/`
3. **Extiende**: Agrega nuevas funcionalidades
4. **Despliega**: Usa `DEPLOYMENT.md` para subirlo a la nube

## 🎓 Recursos

- 📖 **Documentación completa**: Ver `README.md`
- 🚀 **Deployment**: Ver `DEPLOYMENT.md`
- 🔧 **Setup detallado**: Ver `setup_guide.md`
- 🤝 **Contribuir**: Ver `CONTRIBUTING.md`
- 📺 **Videos**: [Canal DacarSoft](https://youtube.com/@DacarSoft)

## 💡 Tips Pro

### Para Desarrollo:

```bash
# Mantén DEBUG=True en .env para ver logs detallados
DEBUG=True

# Usa el modo standalone (más simple)
python main.py --standalone
```

### Para Producción:

```bash
# Cambia a DEBUG=False
DEBUG=False

# Usa el modo con FastAPI (incluye API REST)
python main.py
```

### Ver la API:

Una vez corriendo, abre en tu navegador:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Info: http://localhost:8000/info

## 🎯 Comandos del Bot

Una vez que esté corriendo:

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar el bot |
| `/help` | Ver ayuda y ejemplos |
| `/stats` | Ver estadísticas (próximamente) |

## 💬 Ejemplos de Mensajes

Puedes enviar mensajes naturales como:

### Gastos:
- "Gasté 50 mil en comida"
- "Pagué 15000 en Uber"
- "Compré ropa por 80 mil"
- "Gasté $45000 en supermercado"

### Ingresos:
- "Recibí 100 mil de salario"
- "Ingreso de 250k por freelance"
- "Me pagaron 500 mil por proyecto"

### Presupuestos:
- "Presupuesto de 300 mil para transporte"
- "Presupuesto mensual de 1 millón para arriendo"

¡El bot entiende lenguaje natural en español! 🇪🇸

---

## ⏱️ Resumen de Tiempos

- ⚙️ Instalación local: ~2 min
- 🤖 Crear bot Telegram: ~3 min
- ☁️ Setup Google Cloud: ~10 min
- 🔑 Setup OpenAI: ~5 min
- ⚡ Configurar .env: ~5 min
- ✅ Testing: ~5 min

**Total: ~30 minutos**

---

¿Listo para empezar? ¡Sigue los pasos y tendrás tu bot funcionando en media hora! 🚀

¿Preguntas? Visita [DacarSoft en YouTube](https://youtube.com/@DacarSoft) 📺

