# 🚀 Guía de Configuración Rápida

Esta guía te ayudará a configurar el bot paso a paso.

## ✅ Checklist de Configuración

- [ ] Python 3.11+ instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Bot de Telegram creado
- [ ] Google Cloud Project configurado
- [ ] Google Sheets API habilitada
- [ ] Service Account creado
- [ ] Credentials JSON descargado
- [ ] Spreadsheet creado y compartido
- [ ] OpenAI API Key obtenida
- [ ] Archivo .env configurado
- [ ] Bot ejecutándose correctamente

## 📝 Pasos Detallados

### 1. Preparación del Entorno (10 minutos)

```bash
# Verificar versión de Python
python --version  # Debe ser 3.11 o superior

# Clonar repositorio
git clone https://github.com/dacarsoft/dacarsoft-finance-bot.git
cd dacarsoft-finance-bot

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Bot de Telegram (5 minutos)

1. Abre Telegram y busca `@BotFather`
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot: `Dacarsoft Asistente Financiero Bot`
   - Username: `DacarsoftFinanceBot` (debe terminar en "bot")
4. Copia el token que te proporciona
5. Guarda el token para el paso 5

**Ejemplo de respuesta de BotFather:**
```
Done! Congratulations on your new bot. You will find it at 
t.me/DacarsoftFinanceBot. You can now add a description...

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567

For a description of the Bot API, see this page: 
https://core.telegram.org/bots/api
```

### 3. Configurar Google Sheets (15 minutos)

#### 3.1. Crear Proyecto en Google Cloud

1. Ve a https://console.cloud.google.com/
2. Clic en "Select a project" → "New Project"
3. Nombre: `Dacarsoft Finance Bot`
4. Clic en "Create"

#### 3.2. Habilitar APIs

1. En el menú lateral, ve a "APIs & Services" → "Library"
2. Busca "Google Sheets API" y haz clic en "Enable"
3. Busca "Google Drive API" y haz clic en "Enable"

#### 3.3. Crear Service Account

1. Ve a "APIs & Services" → "Credentials"
2. Clic en "Create Credentials" → "Service Account"
3. Nombre: `dacarsoft-finance-bot`
4. Clic en "Create and Continue"
5. Role: "Editor"
6. Clic en "Done"

#### 3.4. Generar Key JSON

1. Haz clic en el service account que acabas de crear
2. Ve a la pestaña "Keys"
3. Clic en "Add Key" → "Create new key"
4. Selecciona "JSON"
5. Se descargará un archivo JSON
6. Renombra el archivo a `credentials.json`
7. Mueve el archivo a la carpeta `services/` de tu proyecto

#### 3.5. Crear y Compartir Spreadsheet

1. Ve a https://docs.google.com/spreadsheets/
2. Crea un nuevo spreadsheet
3. Nómbralo "Finanzas Dacarsoft"
4. Copia el ID del spreadsheet desde la URL:
   ```
   https://docs.google.com/spreadsheets/d/[ESTE_ES_EL_ID]/edit
   ```
5. Abre el archivo `services/credentials.json`
6. Busca el campo `client_email` (será algo como `xxxxx@xxxxx.iam.gserviceaccount.com`)
7. Comparte el spreadsheet con ese email (dale permisos de Editor)

### 4. Configurar OpenAI (5 minutos)

1. Ve a https://platform.openai.com/
2. Crea una cuenta o inicia sesión
3. Ve a https://platform.openai.com/api-keys
4. Clic en "Create new secret key"
5. Dale un nombre: `Dacarsoft Finance Bot`
6. Copia la key (¡solo la verás una vez!)
7. Guarda la key para el siguiente paso

**Nota:** Necesitarás agregar créditos a tu cuenta de OpenAI. El bot usa GPT-4o-mini que es muy económico (~$0.15 por 1000 mensajes).

### 5. Crear Archivo .env (5 minutos)

Crea un archivo llamado `.env` en la raíz del proyecto con este contenido:

```env
# Telegram Bot Configuration
BOT_NAME="Dacarsoft Asistente Financiero Bot"
BOT_USERNAME="DacarsoftFinanceBot"
BOT_TOKEN="PEGA_AQUI_TU_TOKEN_DE_TELEGRAM"

# Google Sheets Configuration
SHEETS_CREDENTIALS_FILE="services/credentials.json"
SPREADSHEET_ID="PEGA_AQUI_TU_SPREADSHEET_ID"

# OpenAI Configuration
OPENAI_API_KEY="PEGA_AQUI_TU_OPENAI_API_KEY"

# FastAPI Configuration
API_HOST="0.0.0.0"
API_PORT=8000

# Application Configuration
TIMEZONE="America/Bogota"
DEBUG=True
```

**Reemplaza:**
- `PEGA_AQUI_TU_TOKEN_DE_TELEGRAM` con el token de BotFather
- `PEGA_AQUI_TU_SPREADSHEET_ID` con el ID del spreadsheet
- `PEGA_AQUI_TU_OPENAI_API_KEY` con tu OpenAI API key

### 6. Ejecutar el Bot (2 minutos)

```bash
# Asegúrate de que el entorno virtual está activado
python main.py
```

Deberías ver algo como:
```
INFO - Starting Dacarsoft Finance Bot...
INFO - Successfully authenticated with Google Sheets
INFO - Connected to spreadsheet: Finanzas Dacarsoft
INFO - Created sheet: Gastos
INFO - Created sheet: Ingresos
INFO - Created sheet: Presupuestos
INFO - All handlers registered successfully
INFO - Bot started: @DacarsoftFinanceBot
INFO - Uvicorn running on http://0.0.0.0:8000
```

### 7. Probar el Bot (5 minutos)

1. Abre Telegram
2. Busca tu bot por el username que configuraste
3. Envía `/start`
4. Deberías recibir un mensaje de bienvenida
5. Envía: `Gasté 50 mil en comida`
6. El bot debería responder con los detalles de la transacción
7. Verifica que aparece en tu Google Spreadsheet

## 🎉 ¡Felicidades!

Tu bot está funcionando. Ahora puedes:

- Enviar mensajes en lenguaje natural
- Ver tus finanzas en Google Sheets en tiempo real
- Acceder a la API en http://localhost:8000/docs
- Personalizar el bot según tus necesidades

## 🆘 ¿Problemas?

Si algo no funciona, revisa:

1. **Bot no inicia**: Verifica el BOT_TOKEN en .env
2. **Error de Google Sheets**: Verifica que credentials.json existe y que el spreadsheet está compartido
3. **Error de OpenAI**: Verifica que tienes créditos en tu cuenta
4. **Bot no responde**: Revisa los logs en la consola

## 📺 Video Tutorial

Para una explicación visual paso a paso, mira el video en el canal de YouTube [DacarSoft](https://youtube.com/@DacarSoft).

## 💡 Próximos Pasos

- Personaliza los mensajes del bot
- Agrega nuevas categorías
- Implementa estadísticas avanzadas
- Despliega en la nube (Render, Replit, Railway)

---

¿Listo para aprender más? Suscríbete a [DacarSoft en YouTube](https://youtube.com/@DacarSoft)! 🚀

