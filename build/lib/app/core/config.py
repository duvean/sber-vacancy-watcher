from functools import lru_cache

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration read from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Sber Vacancy Watcher"
    debug: bool = False
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/vacancies"
    celery_broker_url: str = "amqp://guest:guest@localhost:5672//"
    celery_result_backend: str = "rpc://"
    sber_api_url: AnyUrl = (
        "https://rabota.sber.ru/public/app-candidate-public-api-gateway/api/v1/publications"
    )
    sber_page_size: int = Field(default=50, ge=1, le=100)
    check_interval_minutes: int = Field(default=15, ge=1, le=1440)
    telegram_bot_token: str = ""
    telegram_api_url: AnyUrl = "https://api.telegram.org"


@lru_cache
def get_settings() -> Settings:
    return Settings()
