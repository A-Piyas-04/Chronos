"""ORM models — import for metadata registration (Alembic, tests)."""

from __future__ import annotations

from app.models.calendar_account import CalendarAccount
from app.models.calendar_event import CalendarEvent
from app.models.enums import (
    CalendarProvider,
    SessionSource,
    SessionStatus,
    TaskPriority,
    TaskStatus,
    TaskType,
)
from app.models.scheduled_session import ScheduledSession
from app.models.task import Task
from app.models.user import User
from app.models.user_preference import UserPreference

__all__ = [
    "CalendarAccount",
    "CalendarEvent",
    "CalendarProvider",
    "ScheduledSession",
    "SessionSource",
    "SessionStatus",
    "Task",
    "TaskPriority",
    "TaskStatus",
    "TaskType",
    "User",
    "UserPreference",
]
