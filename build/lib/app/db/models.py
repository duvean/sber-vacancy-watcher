import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Subscription(TimestampMixin, Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    keywords: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)

    notifications: Mapped[list["Notification"]] = relationship(back_populates="subscription")


class Vacancy(TimestampMixin, Base):
    __tablename__ = "vacancies"

    requisition_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str | None] = mapped_column(String(120), index=True)
    specialization: Mapped[str | None] = mapped_column(String(255))
    introduction: Mapped[str | None] = mapped_column(Text)
    publication_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    source_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)

    notifications: Mapped[list["Notification"]] = relationship(back_populates="vacancy")


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (UniqueConstraint("subscription_id", "vacancy_id", name="uq_notification_subscription_vacancy"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subscription_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subscriptions.id"), nullable=False)
    vacancy_id: Mapped[str] = mapped_column(ForeignKey("vacancies.requisition_id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)

    subscription: Mapped[Subscription] = relationship(back_populates="notifications")
    vacancy: Mapped[Vacancy] = relationship(back_populates="notifications")
