"""Per-user scheduling and display preferences (one row per user)."""

from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String, Time
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class UserPreference(Base, TimestampMixin):
    __tablename__ = "user_preferences"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        doc="IANA timezone name, e.g. America/Los_Angeles",
    )
    workday_start_time: Mapped[time] = mapped_column(Time, nullable=False)
    workday_end_time: Mapped[time] = mapped_column(Time, nullable=False)
    deep_work_start_time: Mapped[time] = mapped_column(Time, nullable=False)
    deep_work_end_time: Mapped[time] = mapped_column(Time, nullable=False)
    max_deep_work_block_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=45,
        server_default="45",
    )

    user: Mapped[User] = relationship(back_populates="preferences")
