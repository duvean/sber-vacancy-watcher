import html

import httpx

from app.core.config import get_settings
from app.db.models import Vacancy


class TelegramClient:
    async def send_vacancy(self, chat_id: int, vacancy: Vacancy) -> None:
        settings = get_settings()
        if not settings.telegram_bot_token or settings.telegram_bot_token == "replace_me":
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

        text = self._build_message(vacancy)
        url = f"{str(settings.telegram_api_url).rstrip('/')}/bot{settings.telegram_bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                url,
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
            )
            response.raise_for_status()

    @staticmethod
    def _build_message(vacancy: Vacancy) -> str:
        title = html.escape(vacancy.title)
        company = html.escape(vacancy.company or "Сбер")
        city = html.escape(vacancy.city or "Не указан")
        description = html.escape((vacancy.introduction or "")[:500])
        return (
            f"<b>Новая вакансия: {title}</b>\n"
            f"Компания: {company}\nГород: {city}\n\n"
            f"{description}\n\n"
            f"ID вакансии: <code>{vacancy.requisition_id}</code>\n"
            '<a href="https://rabota.sber.ru/">Открыть сайт Сбера</a>'
        )
