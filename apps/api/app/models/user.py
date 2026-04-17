"""User account (identity)."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Index, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.calendar_account import CalendarAccount
    from app.models.calendar_event import CalendarEvent
    from app.models.scheduled_session import ScheduledSession
    from app.models.task import Task
    from app.models.user_preference import UserPreference


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            "ix_users_google_sub",
            "google_sub",
            postgresql_where=text("google_sub IS NOT NULL"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    google_sub: Mapped[str | None] = mapped_column(String(255), nullable=True)

    preferences: Mapped[UserPreference | None] = relationship(
        "UserPreference",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    calendar_accounts: Mapped[list[CalendarAccount]] = relationship(
        "CalendarAccount",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    calendar_events: Mapped[list[CalendarEvent]] = relationship(
        "CalendarEvent",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    tasks: Mapped[list[Task]] = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    scheduled_sessions: Mapped[list[ScheduledSession]] = relationship(
        "ScheduledSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
