"""
Telegram bot module.

Contains bot handlers, commands, and message processing logic.
"""

from .handlers import setup_handlers
from .bot_instance import bot_app

__all__ = ["setup_handlers", "bot_app"]

