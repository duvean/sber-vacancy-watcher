from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.db.models import Vacancy
from app.db.session import get_db
from app.schemas.vacancies import QueueResponse, VacancyRead

router = APIRouter(tags=["vacancies"])


@router.get("/vacancies", response_model=list[VacancyRead])
def list_vacancies(
    limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)
) -> list[Vacancy]:
    query = select(Vacancy).order_by(Vacancy.publication_date.desc()).limit(limit)
    return list(db.scalars(query))


@router.post("/jobs/check", response_model=QueueResponse, status_code=202)
def enqueue_check() -> QueueResponse:
    task = celery_app.send_task("app.tasks.vacancies.fetch_and_notify")
    return QueueResponse(task_id=task.id, message="Vacancy check was queued")
