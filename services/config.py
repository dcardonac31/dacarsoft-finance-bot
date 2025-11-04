"""
Configuration management using Pydantic Settings.

Loads configuration from environment variables and .env file.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    To use this application, create a .env file in the project root with:
    - BOT_NAME: Name of your Telegram bot
    - BOT_USERNAME: Username of your Telegram bot
    - BOT_TOKEN: Telegram bot token from @BotFather
    - SHEETS_CREDENTIALS_FILE: Path to Google Sheets credentials JSON
    - SPREADSHEET_ID: Google Sheets spreadsheet ID
    - OPENAI_API_KEY: OpenAI API key for natural language parsing
    """
    
    # Telegram Bot Configuration
    BOT_NAME: str = "Dacarsoft Asistente Financiero Bot"
    BOT_USERNAME: str = "DacarsoftFinanceBot"
    BOT_TOKEN: str
    
    # Google Sheets Configuration
    SHEETS_CREDENTIALS_FILE: str = "services/credentials.json"
    SPREADSHEET_ID: Optional[str] = None
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # FastAPI Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Application Configuration
    TIMEZONE: str = "America/Bogota"
    DEBUG: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def credentials_path(self) -> Path:
        """Get the full path to the Google Sheets credentials file."""
        return Path(self.SHEETS_CREDENTIALS_FILE)


# Global settings instance
settings = Settings()

