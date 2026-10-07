# Sber Vacancy Watcher

Сервис отслеживает новые вакансии в публичном API Сбера и отправляет подходящие вакансии подписчикам Telegram-бота.

Проект использует production-подобный подход: REST API на FastAPI, PostgreSQL + SQLAlchemy/Alembic, RabbitMQ + Celery для фоновой обработки, Docker Compose, валидацию и тесты.

## Развёртывание

1. В `.env` задайте `TELEGRAM_BOT_TOKEN`

2. Поднимите докер:

   ```bash
   docker compose up --build
   ```

   Миграции применяются контейнером `api` перед запуском FastAPI.

3. Откройте Swagger: <http://localhost:8000/docs>.

## Пример работы

Создать подписку:

```bash
curl -X POST http://localhost:8000/api/v1/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_chat_id": 123456789,
    "keywords": ["Python", "ML", "LLM"],
    "city": "Москва"
  }'
```

Запустить проверку немедленно, не дожидаясь расписания:

```bash
curl -X POST http://localhost:8000/api/v1/jobs/check
```

## API

| Метод | Путь | Назначение |
|---|---|---|
| `GET` | `/api/v1/health` | Проверка здоровья приложения |
| `POST` | `/api/v1/subscriptions` | Создание подписки |
| `GET` | `/api/v1/subscriptions/{id}` | Получение подписки |
| `DELETE` | `/api/v1/subscriptions/{id}` | Деактивация подписки |
| `GET` | `/api/v1/vacancies` | Список вакансий, newest first |
| `POST` | `/api/v1/jobs/check` | Поставить проверку в очередь |

## Структура проекта

```text
app/
  api/             # HTTP-слой: роуты и зависимости
  core/            # настройки и экземпляр Celery
  db/              # подключение, ORM-модели, миграции
  schemas/         # Pydantic-схемы запросов/ответов
  services/        # бизнес-логика: Sber API, matching, Telegram
  tasks/           # Celery-задачи
tests/             # unit-тесты бизнес-логики и API
```

---

## Автор

**duvean**

[GitHub](https://github.com/duvean)
