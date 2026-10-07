from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "sber_vacancy_watcher",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.vacancies"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    task_track_started=True,
    broker_connection_retry_on_startup=True,
    beat_schedule={
        "fetch-new-vacancies": {
            "task": "app.tasks.vacancies.fetch_and_notify",
            "schedule": settings.check_interval_minutes * 60,
        }
    },
)
