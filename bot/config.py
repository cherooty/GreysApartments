"""Глобальные настройки (pydantic-settings)."""

from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field

class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    database_url: PostgresDsn = Field(..., env="DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

@lru_cache()
def get_settings() -> "Settings":
    return Settings()

settings = get_settings()
