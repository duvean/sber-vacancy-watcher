from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SubscriptionCreate(BaseModel):
    telegram_chat_id: int
    keywords: list[str] = Field(default_factory=list, max_length=10)
    city: str | None = Field(default=None, max_length=120)

    @field_validator("keywords")
    @classmethod
    def normalize_keywords(cls, value: list[str]) -> list[str]:
        normalized = list(dict.fromkeys(item.strip().lower() for item in value if item.strip()))
        if not normalized:
            raise ValueError("Укажите хотя бы одно непустое ключевое слово")
        return normalized


class SubscriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_chat_id: int
    keywords: list[str]
    city: str | None
    is_active: bool
    created_at: datetime


class SubscriptionDeleted(BaseModel):
    id: UUID
    is_active: bool
