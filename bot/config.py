"""Application settings, loaded from environment / .env at startup."""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Telegram ---
    bot_token: SecretStr
    drop_pending_updates: bool = True

    # --- Storage ---
    # Postgres DSN for the async driver, e.g.
    # postgresql+asyncpg://bot:bot@localhost:5432/bot
    db_dsn: str
    db_echo: bool = False

    # When unset, FSM state lives in memory and is lost on restart.
    redis_dsn: str | None = None

    # --- Behaviour ---
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Cached accessor so settings are validated exactly once per process."""
    return Settings()  # type: ignore[call-arg]  # values come from the environment
