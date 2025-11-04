"""
Telegram bot application instance.

Creates and configures the Telegram bot application.
"""

import logging
from telegram.ext import Application

from services.config import settings

logger = logging.getLogger(__name__)


def create_bot_application() -> Application:
    """
    Create and configure the Telegram bot application.
    
    Returns:
        Configured Application instance
    """
    # Create application
    app = Application.builder().token(settings.BOT_TOKEN).build()
    
    logger.info(f"Created bot application: {settings.BOT_NAME}")
    return app


# Global bot application instance
bot_app = create_bot_application()

