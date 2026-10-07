from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VacancyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    requisition_id: str
    title: str
    company: str | None
    city: str | None
    specialization: str | None
    publication_date: datetime | None


class QueueResponse(BaseModel):
    task_id: str
    message: str
