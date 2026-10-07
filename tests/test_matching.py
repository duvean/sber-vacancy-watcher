from app.db.models import Subscription, Vacancy
from app.services.matching import matches_subscription


def make_vacancy(**overrides) -> Vacancy:
    data = {
        "requisition_id": "vacancy-1",
        "title": "Python Backend Developer",
        "city": "г Москва",
        "specialization": "Информационные технологии",
        "introduction": "Разработка сервисов на FastAPI",
        "source_payload": {},
    }
    data.update(overrides)
    return Vacancy(**data)


def test_matches_keyword_and_city() -> None:
    subscription = Subscription(telegram_chat_id=42, keywords=["python", "fastapi"], city="Москва")

    assert matches_subscription(make_vacancy(), subscription) is True


def test_does_not_match_another_city() -> None:
    subscription = Subscription(telegram_chat_id=42, keywords=["python"], city="Санкт-Петербург")

    assert matches_subscription(make_vacancy(), subscription) is False


def test_matches_keyword_from_description() -> None:
    subscription = Subscription(telegram_chat_id=42, keywords=["fastapi"])

    assert matches_subscription(make_vacancy(title="Backend developer"), subscription) is True
