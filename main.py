"""
Main entry point for Dacarsoft Finance Bot.

Starts the Telegram bot and optional FastAPI server.
"""

import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from telegram import Update
from telegram.ext import Application

from bot.handlers import setup_handlers, initialize_services
from bot.bot_instance import bot_app
from services.config import settings

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if settings.DEBUG else logging.WARNING
)

logger = logging.getLogger(__name__)


# FastAPI application with lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    
    Handles startup and shutdown of the Telegram bot.
    """
    # Startup
    logger.info("Starting Dacarsoft Finance Bot...")
    
    # Initialize services (Google Sheets)
    if not initialize_services():
        logger.error("Failed to initialize services. Bot may not function correctly.")
    
    # Setup bot handlers
    setup_handlers(bot_app)
    
    # Start the bot
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling(drop_pending_updates=True)
    
    logger.info(f"Bot started successfully: @{settings.BOT_USERNAME}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down bot...")
    await bot_app.updater.stop()
    await bot_app.stop()
    await bot_app.shutdown()
    logger.info("Bot stopped")


# Create FastAPI app
app = FastAPI(
    title="Dacarsoft Finance Bot API",
    description="REST API for Dacarsoft Finance Bot",
    version="1.0.0",
    lifespan=lifespan
)


# API Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.BOT_NAME,
        "username": settings.BOT_USERNAME,
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "bot_running": bot_app.running
    }


@app.get("/info")
async def bot_info():
    """Get bot information."""
    try:
        bot = await bot_app.bot.get_me()
        return {
            "id": bot.id,
            "username": bot.username,
            "first_name": bot.first_name,
            "can_join_groups": bot.can_join_groups,
            "can_read_all_group_messages": bot.can_read_all_group_messages
        }
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return {"error": str(e)}


async def run_bot_standalone():
    """
    Run the bot in standalone mode (without FastAPI).
    
    Use this if you don't need the REST API.
    """
    logger.info("Starting bot in standalone mode...")
    
    # Initialize services
    if not initialize_services():
        logger.error("Failed to initialize services. Exiting.")
        return
    
    # Setup handlers
    setup_handlers(bot_app)
    
    # Start the bot
    await bot_app.initialize()
    await bot_app.start()
    
    logger.info(f"Bot started: @{settings.BOT_USERNAME}")
    logger.info("Press Ctrl+C to stop")
    
    # Start polling
    await bot_app.updater.start_polling(drop_pending_updates=True)
    
    # Run until interrupted
    try:
        # Keep the bot running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        # Cleanup
        await bot_app.updater.stop()
        await bot_app.stop()
        await bot_app.shutdown()
        logger.info("Bot stopped")


def main():
    """
    Main entry point.
    
    Choose between FastAPI mode (with REST API) or standalone mode (bot only).
    """
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--standalone":
        # Run bot in standalone mode
        asyncio.run(run_bot_standalone())
    else:
        # Run with FastAPI (default)
        import uvicorn
        uvicorn.run(
            "main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=settings.DEBUG
        )


if __name__ == "__main__":
    main()

