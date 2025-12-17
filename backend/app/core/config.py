# backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # AI API Keys (using Groq instead of Gemini)
    GROQ_API_KEY: str
    GEMINI_API_KEY: Optional[str] = None  # Optional, kept for backwards compatibility
    
    DATABASE_URL: str

    # Twitter Keys (optional for demo)
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None

settings = Settings()