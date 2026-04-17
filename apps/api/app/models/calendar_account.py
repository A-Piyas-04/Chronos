"""Linked calendar provider account (OAuth tokens stored as placeholders until crypto layer exists)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import CalendarProvider

if TYPE_CHECKING:
    from app.models.calendar_event import CalendarEvent
    from app.models.user import User


class CalendarAccount(Base, TimestampMixin):
    __tablename__ = "calendar_accounts"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "provider",
            "provider_account_id",
            name="uq_calendar_accounts_user_provider_account",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider: Mapped[CalendarProvider] = mapped_column(
        SAEnum(CalendarProvider, name="calendar_provider", native_enum=True),
        nullable=False,
    )
    provider_account_id: Mapped[str] = mapped_column(String(512), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    access_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Opaque or encrypted secret; do not log.",
    )
    refresh_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Opaque or encrypted secret; do not log.",
    )
    token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped[User] = relationship(back_populates="calendar_accounts")
    events: Mapped[list[CalendarEvent]] = relationship(
        back_populates="calendar_account",
        cascade="all, delete-orphan",
    )
