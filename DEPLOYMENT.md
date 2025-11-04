# 🚀 Guía de Deployment

Esta guía explica cómo desplegar el bot en diferentes plataformas cloud.

## 📋 Índice

- [Render.com](#rendercom)
- [Replit](#replit)
- [Railway.app](#railwayapp)
- [Heroku](#heroku)
- [VPS (Digital Ocean, AWS EC2, etc.)](#vps)

---

## Render.com

Render es una plataforma moderna y fácil de usar para desplegar aplicaciones.

### Pasos:

1. **Preparar el repositorio**
   - Haz commit de todos tus cambios
   - Push a GitHub

2. **Crear cuenta en Render**
   - Ve a [render.com](https://render.com)
   - Crea una cuenta (puede ser con GitHub)

3. **Crear nuevo Web Service**
   - Clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona el repo `dacarsoft-finance-bot`

4. **Configurar el servicio**
   ```
   Name: dacarsoft-finance-bot
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   ```

5. **Configurar variables de entorno**
   
   En la sección "Environment Variables", agrega:
   ```
   BOT_NAME=Dacarsoft Asistente Financiero Bot
   BOT_USERNAME=DacarsoftFinanceBot
   BOT_TOKEN=tu_telegram_token
   SPREADSHEET_ID=tu_spreadsheet_id
   OPENAI_API_KEY=tu_openai_key
   SHEETS_CREDENTIALS_FILE=services/credentials.json
   API_HOST=0.0.0.0
   API_PORT=10000
   TIMEZONE=America/Bogota
   DEBUG=False
   ```

6. **Subir credentials.json**
   
   Render necesita el archivo de credenciales. Tienes dos opciones:
   
   **Opción A: Secret Files**
   - En Render Dashboard, ve a "Settings" → "Secret Files"
   - Crea un nuevo archivo secreto
   - Filename: `services/credentials.json`
   - Contents: Pega el contenido de tu archivo credentials.json
   
   **Opción B: Codificar en base64**
   - Convierte credentials.json a base64
   - Guárdalo como variable de entorno `GOOGLE_CREDENTIALS_BASE64`
   - Modifica `services/config.py` para decodificarlo

7. **Deploy**
   - Clic en "Create Web Service"
   - Render automáticamente desplegará tu bot

8. **Verificar**
   - Ve a los logs para verificar que el bot inició correctamente
   - Prueba tu bot en Telegram

### Nota importante para Render:
Render puede suspender servicios gratuitos después de 15 minutos de inactividad. Para mantener el bot activo 24/7, necesitarás un plan pago ($7/mes).

---

## Replit

Replit es ideal para desarrollo rápido y prototipos.

### Pasos:

1. **Crear cuenta**
   - Ve a [replit.com](https://replit.com)
   - Crea una cuenta

2. **Importar proyecto**
   - Clic en "+ Create Repl"
   - Selecciona "Import from GitHub"
   - Pega la URL de tu repositorio

3. **Configurar Secrets**
   
   En el panel izquierdo, busca "Secrets" (🔒) y agrega:
   ```
   BOT_TOKEN=tu_telegram_token
   SPREADSHEET_ID=tu_spreadsheet_id
   OPENAI_API_KEY=tu_openai_key
   ```

4. **Subir credentials.json**
   - Crea la carpeta `services/` si no existe
   - Sube el archivo `credentials.json` a esa carpeta

5. **Configurar .replit**
   
   Crea un archivo `.replit` en la raíz:
   ```toml
   run = "python main.py"
   
   [nix]
   channel = "stable-23_05"
   
   [deployment]
   run = ["sh", "-c", "python main.py"]
   ```

6. **Ejecutar**
   - Clic en "Run"
   - El bot debería iniciar automáticamente

7. **Mantener activo (Always On)**
   - Para mantener el bot corriendo 24/7, necesitas Replit Hacker plan ($7/mes)
   - O usa un servicio de ping externo (UptimeRobot) para mantenerlo activo

---

## Railway.app

Railway es moderno y ofrece despliegues rápidos con Git.

### Pasos:

1. **Crear cuenta**
   - Ve a [railway.app](https://railway.app)
   - Inicia sesión con GitHub

2. **Crear nuevo proyecto**
   - Clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio

3. **Configurar variables de entorno**
   
   En Settings → Variables:
   ```
   BOT_TOKEN=tu_telegram_token
   SPREADSHEET_ID=tu_spreadsheet_id
   OPENAI_API_KEY=tu_openai_key
   BOT_NAME=Dacarsoft Asistente Financiero Bot
   BOT_USERNAME=DacarsoftFinanceBot
   SHEETS_CREDENTIALS_FILE=services/credentials.json
   DEBUG=False
   ```

4. **Subir credentials.json**
   - Railway detecta automáticamente archivos en el repo
   - Asegúrate de que `credentials.json` NO esté en `.gitignore` para Railway
   - O usa Railway Volumes para archivos persistentes

5. **Configurar Procfile** (opcional)
   
   Crea `Procfile` en la raíz:
   ```
   web: python main.py
   ```

6. **Deploy**
   - Railway desplegará automáticamente en cada push
   - Monitorea los logs en el dashboard

---

## Heroku

Heroku es una plataforma clásica y confiable.

### Pasos:

1. **Instalar Heroku CLI**
   ```bash
   # Windows (con chocolatey)
   choco install heroku-cli
   
   # Mac
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Crear app**
   ```bash
   heroku create dacarsoft-finance-bot
   ```

4. **Configurar buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

5. **Crear Procfile**
   
   Crea `Procfile` en la raíz:
   ```
   web: python main.py
   ```

6. **Crear runtime.txt**
   
   Especifica la versión de Python:
   ```
   python-3.11.6
   ```

7. **Configurar variables de entorno**
   ```bash
   heroku config:set BOT_TOKEN=tu_telegram_token
   heroku config:set SPREADSHEET_ID=tu_spreadsheet_id
   heroku config:set OPENAI_API_KEY=tu_openai_key
   heroku config:set BOT_NAME="Dacarsoft Asistente Financiero Bot"
   heroku config:set BOT_USERNAME="DacarsoftFinanceBot"
   heroku config:set DEBUG=False
   ```

8. **Subir credentials.json**
   
   Opción con buildpack:
   ```bash
   # Instala el buildpack de Google credentials
   heroku buildpacks:add https://github.com/elishaterada/heroku-google-application-credentials-buildpack
   
   # Configura la variable
   heroku config:set GOOGLE_CREDENTIALS="$(cat services/credentials.json)"
   heroku config:set GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
   ```

9. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

10. **Ver logs**
    ```bash
    heroku logs --tail
    ```

---

## VPS (Digital Ocean, AWS EC2, Linode, etc.)

Para control total, usa un VPS.

### Pasos (Ubuntu 22.04):

1. **Conectar al servidor**
   ```bash
   ssh root@tu_ip_del_servidor
   ```

2. **Actualizar sistema**
   ```bash
   apt update && apt upgrade -y
   ```

3. **Instalar Python 3.11**
   ```bash
   apt install python3.11 python3.11-venv python3-pip -y
   ```

4. **Crear usuario para el bot**
   ```bash
   adduser botuser
   usermod -aG sudo botuser
   su - botuser
   ```

5. **Clonar repositorio**
   ```bash
   cd ~
   git clone https://github.com/dacarsoft/dacarsoft-finance-bot.git
   cd dacarsoft-finance-bot
   ```

6. **Crear entorno virtual**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

7. **Configurar .env**
   ```bash
   nano .env
   # Pega tu configuración y guarda (Ctrl+X, Y, Enter)
   ```

8. **Subir credentials.json**
   ```bash
   # Desde tu máquina local:
   scp services/credentials.json botuser@tu_ip:/home/botuser/dacarsoft-finance-bot/services/
   ```

9. **Probar el bot**
   ```bash
   python main.py
   # Ctrl+C para detener
   ```

10. **Configurar systemd para auto-inicio**
    
    Crea `/etc/systemd/system/financebot.service`:
    ```ini
    [Unit]
    Description=Dacarsoft Finance Bot
    After=network.target
    
    [Service]
    Type=simple
    User=botuser
    WorkingDirectory=/home/botuser/dacarsoft-finance-bot
    Environment="PATH=/home/botuser/dacarsoft-finance-bot/venv/bin"
    ExecStart=/home/botuser/dacarsoft-finance-bot/venv/bin/python main.py
    Restart=always
    RestartSec=10
    
    [Install]
    WantedBy=multi-user.target
    ```

11. **Activar el servicio**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable financebot
    sudo systemctl start financebot
    ```

12. **Ver logs**
    ```bash
    sudo journalctl -u financebot -f
    ```

13. **Comandos útiles**
    ```bash
    # Ver estado
    sudo systemctl status financebot
    
    # Reiniciar
    sudo systemctl restart financebot
    
    # Detener
    sudo systemctl stop financebot
    
    # Ver logs
    sudo journalctl -u financebot -n 100
    ```

---

## 🔒 Seguridad

### Mejores prácticas para producción:

1. **Nunca commits credenciales**
   ```bash
   # Verifica que .gitignore incluye:
   .env
   services/credentials.json
   ```

2. **Usa variables de entorno**
   - Todas las plataformas soportan variables de entorno
   - Nunca hardcodees tokens o keys

3. **Restringe acceso a Google Sheets**
   - Solo comparte con el service account necesario
   - No hagas el spreadsheet público

4. **Monitorea uso de APIs**
   - OpenAI: Configura límites de gasto
   - Google: Monitorea quotas

5. **Logs y monitoring**
   - Configura alertas para errores
   - Revisa logs regularmente

---

## 💰 Costos Estimados

### Hosting:

- **Replit Hacker**: $7/mes (always-on)
- **Render Basic**: $7/mes (always-on)
- **Railway**: ~$5/mes (pay-as-you-go)
- **Heroku Hobby**: $7/mes
- **Digital Ocean Droplet**: $5-6/mes (básico)
- **AWS EC2 t2.micro**: Gratis por 12 meses, luego ~$8/mes

### APIs:

- **Google Sheets**: Gratis (hasta 500 requests/100 segundos)
- **OpenAI GPT-4o-mini**: ~$0.15 por 1000 mensajes
- **Telegram Bot**: 100% Gratis

### Total estimado: $7-12/mes (hosting) + ~$5/mes (OpenAI para uso personal)

---

## 📊 Monitoreo

### UptimeRobot (gratuito)

Para mantener el bot activo en plataformas gratuitas:

1. Ve a [uptimerobot.com](https://uptimerobot.com)
2. Crea un monitor HTTP(S)
3. URL: Tu endpoint `/health`
4. Intervalo: 5 minutos

### Healthchecks.io

Alternativa moderna:

1. Ve a [healthchecks.io](https://healthchecks.io)
2. Crea un nuevo check
3. Configura el bot para hacer ping periódicamente

---

## 🆘 Troubleshooting en Producción

### Bot no responde

1. Verifica logs de la plataforma
2. Confirma que el servicio está corriendo
3. Verifica conectividad de red

### Error de Google Sheets

1. Verifica que credentials.json se subió correctamente
2. Confirma que el spreadsheet está compartido
3. Revisa quotas de Google Cloud

### Error de OpenAI

1. Verifica saldo de la cuenta
2. Confirma que la API key es válida
3. Revisa rate limits

---

## 🎓 Recursos Adicionales

- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

¿Preguntas? Visita el canal de YouTube [DacarSoft](https://youtube.com/@DacarSoft) para tutoriales detallados! 🚀

