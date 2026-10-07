from fastapi import FastAPI

from app.api.routes import health, subscriptions, vacancies
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Watch Sber vacancies and notify Telegram subscribers.",
)
app.include_router(health.router, prefix="/api/v1")
app.include_router(subscriptions.router, prefix="/api/v1")
app.include_router(vacancies.router, prefix="/api/v1")
