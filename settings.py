import os
from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/bot")

    def _normalize_database_url(self, url: str) -> str:
        """Приводит Railway URL к формату, понятному SQLAlchemy + asyncpg."""
        url = url.strip()
        # Railway иногда даёт postgres:// вместо postgresql://
        if url.startswith("postgres://"):
            url = "postgresql" + url[len("postgres"):]
        # Если asyncpg ещё не указан, добавляем его
        if url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    # LLM
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-sonnet-4.6")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "")

    # Modes
    ENABLE_BUSINESS_MODE: bool = os.getenv("ENABLE_BUSINESS_MODE", "true").lower() == "true"
    ENABLE_DIRECT_MODE: bool = os.getenv("ENABLE_DIRECT_MODE", "true").lower() == "true"

    # Settings
    MAX_CONTEXT_MESSAGES: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "20"))
    DEFAULT_PROMPT_ID: int = int(os.getenv("DEFAULT_PROMPT_ID", "1"))

    # Admin — необязательно, по умолчанию пустой список
    ADMIN_IDS: list[int] = []

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def _parse_admin_ids(cls, v: Any) -> list[int]:
        """Принимает список, одно число или строку через запятую."""
        if v is None or v == "":
            return []
        if isinstance(v, int):
            return [v]
        if isinstance(v, list):
            return [int(x) for x in v if x is not None]
        if isinstance(v, str):
            try:
                return [int(x.strip()) for x in v.split(",") if x.strip()]
            except ValueError:
                return []
        return []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Приводим DATABASE_URL к формату asyncpg (важно для Railway)
        self.DATABASE_URL = self._normalize_database_url(self.DATABASE_URL)

    class Config:
        env_file = ".env"


settings = Settings()
