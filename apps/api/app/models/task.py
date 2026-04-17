"""User tasks for scheduling."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import TaskPriority, TaskStatus, TaskType

if TYPE_CHECKING:
    from app.models.scheduled_session import ScheduledSession
    from app.models.user import User


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"
    __table_args__ = (Index("ix_tasks_user_status", "user_id", "status"),)

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
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    estimated_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    remaining_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    deadline_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority, name="task_priority", native_enum=True),
        nullable=False,
    )
    task_type: Mapped[TaskType | None] = mapped_column(
        SAEnum(TaskType, name="task_type", native_enum=True),
        nullable=True,
    )
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status", native_enum=True),
        nullable=False,
        default=TaskStatus.inbox,
    )

    user: Mapped[User] = relationship(back_populates="tasks")
    scheduled_sessions: Mapped[list[ScheduledSession]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
    )
