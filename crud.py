import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/bot")

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Парсим ADMIN_IDS вручную
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if admin_ids_str:
            try:
                self.ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()]
            except ValueError:
                self.ADMIN_IDS = []

    class Config:
        env_file = ".env"


settings = Settings()
