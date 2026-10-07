import pytest
from pydantic import ValidationError

from app.schemas.subscriptions import SubscriptionCreate


def test_subscription_normalizes_keywords() -> None:
    payload = SubscriptionCreate(telegram_chat_id=10, keywords=[" Python ", "python", "FastAPI"])

    assert payload.keywords == ["python", "fastapi"]


def test_subscription_rejects_empty_keywords() -> None:
    with pytest.raises(ValidationError):
        SubscriptionCreate(telegram_chat_id=10, keywords=[" "])
