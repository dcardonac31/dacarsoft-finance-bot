"""
Telegram bot command and message handlers.

Implements bot commands (/start, /help, etc.) and message processing.
"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from services.llm_service import LLMService
from services.sheets_service import SheetsService
from services.config import settings

logger = logging.getLogger(__name__)

# Initialize services
llm_service = LLMService()
sheets_service = SheetsService()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    
    Sends a welcome message to the user.
    """
    welcome_message = (
        "👋 ¡Hola! Soy Dacarsoft Asistente Financiero Bot.\n\n"
        "Te ayudaré a registrar tus gastos, ingresos y presupuestos.\n\n"
        "📝 Simplemente envíame mensajes como:\n"
        "• \"Gasté 50 mil en comida\"\n"
        "• \"Recibí 100 mil de salario\"\n"
        "• \"Presupuesto de 300 mil para transporte\"\n\n"
        "Usa /help para ver más información."
    )
    
    await update.message.reply_text(welcome_message)
    logger.info(f"User {update.effective_user.id} started the bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command.
    
    Provides usage instructions and examples.
    """
    help_message = (
        "🤖 *Cómo usar el bot*\n\n"
        "Envíame mensajes en lenguaje natural sobre tus finanzas:\n\n"
        "*Gastos:*\n"
        "• Gasté 50 mil en comida\n"
        "• Pagué 15000 en Uber\n"
        "• Compré ropa por 80 mil\n\n"
        "*Ingresos:*\n"
        "• Recibí 100 mil de salario\n"
        "• Ingreso de 250k por freelance\n\n"
        "*Presupuestos:*\n"
        "• Presupuesto de 300 mil para transporte\n"
        "• Presupuesto mensual de 1 millón para arriendo\n\n"
        "*Ahorros e Inversiones:* 💰\n"
        "• Ahorré 100 mil en el banco\n"
        "• Invertí 500 mil en CDT\n"
        "• Guardé 200k en Davivienda\n\n"
        "*Comandos disponibles:*\n"
        "/start - Iniciar el bot\n"
        "/help - Ver esta ayuda\n"
        "/stats - Ver estadísticas (próximamente)\n\n"
        "💡 *Tip:* Puedes usar \"mil\", \"k\" o números directos"
    )
    
    await update.message.reply_text(help_message, parse_mode='Markdown')
    logger.info(f"User {update.effective_user.id} requested help")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /stats command.
    
    Shows user statistics (to be implemented).
    """
    stats_message = (
        "📊 *Estadísticas*\n\n"
        "Esta función estará disponible próximamente.\n\n"
        "Aquí podrás ver:\n"
        "• Total de gastos\n"
        "• Total de ingresos\n"
        "• Presupuesto vs. gastos reales\n"
        "• Gastos por categoría"
    )
    
    await update.message.reply_text(stats_message, parse_mode='Markdown')
    logger.info(f"User {update.effective_user.id} requested stats")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle regular text messages.
    
    Parses the message using LLM and saves to Google Sheets.
    Handles both transactions (gastos/ingresos/presupuestos) and capital movements (ahorros/inversiones).
    """
    user_message = update.message.text
    user_id = update.effective_user.id
    
    logger.info(f"Received message from user {user_id}: {user_message}")
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    try:
        # Parse message with LLM - returns (object, type)
        result, result_type = await llm_service.parse_message(user_message)
        
        if not result:
            error_message = (
                "❌ Lo siento, no pude entender tu mensaje.\n\n"
                "Por favor, intenta con un mensaje como:\n"
                "• \"Gasté 50 mil en comida\"\n"
                "• \"Recibí 100 mil de salario\"\n"
                "• \"Presupuesto de 300 mil para transporte\"\n"
                "• \"Ahorré 100 mil en el banco\" 💰\n\n"
                "Usa /help para ver más ejemplos."
            )
            await update.message.reply_text(error_message)
            return
        
        # Save to appropriate Google Sheets location
        if result_type == "capital":
            # It's a capital movement (ahorro/inversion)
            success = sheets_service.save_capital_movement(result)
            
            if success:
                tipo_emoji = {
                    "ahorro": "🏦",
                    "inversion": "📈"
                }
                
                success_message = (
                    f"✅ ¡Registrado!\n\n"
                    f"{tipo_emoji.get(result.tipo.value, '💰')} *{result.tipo.value.capitalize()}*\n"
                    f"💵 Monto: ${result.monto:,.2f}\n"
                    f"🏢 Institución: {result.institucion}\n"
                    f"📝 Descripción: {result.descripcion or 'N/A'}\n"
                    f"📅 Fecha: {result.fecha.strftime('%Y-%m-%d %H:%M')}\n"
                    f"✅ Estado: {result.estado.value}"
                )
                
                await update.message.reply_text(success_message, parse_mode='Markdown')
                logger.info(f"Successfully saved capital movement for user {user_id}")
            else:
                error_message = (
                    "❌ Error al guardar el movimiento de capital.\n\n"
                    "Por favor, intenta de nuevo o contacta al administrador."
                )
                await update.message.reply_text(error_message)
                logger.error(f"Failed to save capital movement for user {user_id}")
        
        else:
            # It's a regular transaction (gasto/ingreso/presupuesto)
            success = sheets_service.save_transaction(result)
            
            if success:
                tipo_emoji = {
                    "gasto": "💸",
                    "ingreso": "💰",
                    "presupuesto": "📊"
                }
                
                success_message = (
                    f"✅ ¡Registrado!\n\n"
                    f"{tipo_emoji.get(result.tipo.value, '📝')} *{result.tipo.value.capitalize()}*\n"
                    f"💵 Monto: ${result.monto:,.2f}\n"
                    f"📁 Categoría: {result.categoria}\n"
                    f"📝 Descripción: {result.descripcion or 'N/A'}\n"
                    f"📅 Fecha: {result.fecha.strftime('%Y-%m-%d %H:%M')}"
                )
                
                await update.message.reply_text(success_message, parse_mode='Markdown')
                logger.info(f"Successfully saved transaction for user {user_id}")
            else:
                error_message = (
                    "❌ Error al guardar la transacción.\n\n"
                    "Por favor, intenta de nuevo o contacta al administrador."
                )
                await update.message.reply_text(error_message)
                logger.error(f"Failed to save transaction for user {user_id}")
            
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_message = (
            "❌ Ocurrió un error al procesar tu mensaje.\n\n"
            "Por favor, intenta de nuevo."
        )
        await update.message.reply_text(error_message)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors in the bot.
    
    Logs errors and notifies the user if applicable.
    """
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    
    # If the error occurred during message processing, notify the user
    if isinstance(update, Update) and update.effective_message:
        error_message = (
            "❌ Ocurrió un error inesperado.\n\n"
            "El equipo técnico ha sido notificado."
        )
        try:
            await update.effective_message.reply_text(error_message)
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}")


def setup_handlers(application: Application) -> None:
    """
    Set up all bot handlers.
    
    Args:
        application: The Telegram Application instance
    """
    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Message handler for regular text messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    
    # Error handler
    application.add_error_handler(error_handler)
    
    logger.info("All handlers registered successfully")


def initialize_services() -> bool:
    """
    Initialize external services (Google Sheets).
    
    Returns:
        True if initialization successful, False otherwise
    """
    try:
        # Authenticate with Google Sheets
        if not sheets_service.authenticate():
            logger.error("Failed to authenticate with Google Sheets")
            return False
        
        # Connect to spreadsheet
        if not sheets_service.connect_spreadsheet():
            logger.error("Failed to connect to spreadsheet")
            return False
        
        # Initialize sheets structure
        if not sheets_service.initialize_sheets():
            logger.error("Failed to initialize sheets")
            return False
        
        logger.info("All services initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing services: {e}", exc_info=True)
        return False

