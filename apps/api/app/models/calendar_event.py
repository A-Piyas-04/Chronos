"""Imported calendar events (read-only sync in a later phase)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.calendar_account import CalendarAccount
    from app.models.user import User


class CalendarEvent(Base, TimestampMixin):
    __tablename__ = "calendar_events"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "external_event_id",
            name="uq_calendar_events_user_external_event",
        ),
        Index("ix_calendar_events_user_start", "user_id", "start_at"),
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
    calendar_account_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("calendar_accounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    external_event_id: Mapped[str] = mapped_column(String(1024), nullable=False)
    source_calendar_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False, default="", server_default="")
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_all_day: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    is_busy: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    raw_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped[User] = relationship(back_populates="calendar_events")
    calendar_account: Mapped[CalendarAccount | None] = relationship(
        back_populates="events",
    )
