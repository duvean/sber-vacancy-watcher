import asyncio
import logging
from datetime import datetime, timezone

from celery import shared_task
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.models import Notification, Subscription, Vacancy
from app.db.session import SessionLocal
from app.services.matching import matches_subscription
from app.services.sber_client import SberApiClient, SberVacancy
from app.services.telegram import TelegramClient

logger = logging.getLogger(__name__)


def _save_new_vacancy(db, item: SberVacancy) -> Vacancy | None:
    """Insert an external vacancy once; return None if it has already been processed."""
    if db.get(Vacancy, item.requisition_id):
        return None
    vacancy = Vacancy(
        requisition_id=item.requisition_id,
        title=item.title,
        company=item.company,
        city=item.city,
        specialization=item.specialization,
        introduction=item.introduction,
        publication_date=item.publication_date,
        source_payload=item.model_dump(mode="json", by_alias=True),
    )
    db.add(vacancy)
    db.flush()
    return vacancy


@shared_task(name="app.tasks.vacancies.fetch_and_notify", bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def fetch_and_notify(self) -> dict[str, int]:
    """Fetch latest vacancies, persist unseen records and enqueue matching notifications."""
    items = asyncio.run(SberApiClient().fetch_latest())
    notifications_to_deliver: list[int] = []
    new_vacancies = 0

    with SessionLocal() as db:
        subscriptions = list(db.scalars(select(Subscription).where(Subscription.is_active.is_(True))))
        for item in items:
            vacancy = _save_new_vacancy(db, item)
            if vacancy is None:
                continue
            new_vacancies += 1
            for subscription in subscriptions:
                if not matches_subscription(vacancy, subscription):
                    continue
                notification = Notification(subscription=subscription, vacancy=vacancy)
                db.add(notification)
                db.flush()
                notifications_to_deliver.append(notification.id)
        db.commit()

    for notification_id in notifications_to_deliver:
        deliver_notification.delay(notification_id)
    logger.info("Found %s new vacancies; queued %s notifications", new_vacancies, len(notifications_to_deliver))
    return {"new_vacancies": new_vacancies, "notifications": len(notifications_to_deliver)}


@shared_task(
    name="app.tasks.vacancies.deliver_notification",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def deliver_notification(self, notification_id: int) -> None:
    """Send exactly one notification; failed deliveries can be safely retried."""
    with SessionLocal() as db:
        notification = db.scalar(
            select(Notification)
            .options(joinedload(Notification.subscription), joinedload(Notification.vacancy))
            .where(Notification.id == notification_id)
        )
        if notification is None or notification.status == "sent":
            return
        try:
            asyncio.run(
                TelegramClient().send_vacancy(notification.subscription.telegram_chat_id, notification.vacancy)
            )
            notification.status = "sent"
            notification.sent_at = datetime.now(timezone.utc)
            notification.error_message = None
            db.commit()
        except Exception as exc:
            notification.status = "failed"
            notification.error_message = str(exc)[:1000]
            db.commit()
            raise
