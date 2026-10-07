from datetime import datetime
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field

from app.core.config import get_settings


class SberVacancy(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    requisition_id: str = Field(alias="requisitionId")
    title: str
    company: str | None = None
    city: str | None = None
    specialization: str | None = None
    introduction: str | None = None
    publication_date: datetime | None = Field(default=None, alias="publicationDate")


class SberApiClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or str(get_settings().sber_api_url)

    async def fetch_latest(self) -> list[SberVacancy]:
        settings = get_settings()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                self.base_url, params={"skip": 0, "take": settings.sber_page_size}
            )
            response.raise_for_status()
        payload: dict[str, Any] = response.json()
        records = payload.get("data", {}).get("vacancies", [])
        return [SberVacancy.model_validate(record) for record in records]
