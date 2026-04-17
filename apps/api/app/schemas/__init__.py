"""Pydantic request/response models for HTTP APIs."""

from __future__ import annotations

from app.schemas.base import OrmSchema
from app.schemas.calendar import (
    CalendarAccountCreate,
    CalendarAccountRead,
    CalendarAccountUpdate,
    CalendarEventCreate,
    CalendarEventRead,
    CalendarEventUpdate,
    calendar_account_to_read,
    calendar_event_to_read,
)
from app.schemas.session import (
    ScheduledSessionCreate,
    ScheduledSessionRead,
    ScheduledSessionUpdate,
)
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.schemas.user import (
    UserCreate,
    UserPreferenceCreate,
    UserPreferenceRead,
    UserPreferenceUpdate,
    UserRead,
    UserUpdate,
)

__all__ = [
    "CalendarAccountCreate",
    "CalendarAccountRead",
    "CalendarAccountUpdate",
    "CalendarEventCreate",
    "CalendarEventRead",
    "CalendarEventUpdate",
    "OrmSchema",
    "ScheduledSessionCreate",
    "ScheduledSessionRead",
    "ScheduledSessionUpdate",
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    "UserCreate",
    "UserPreferenceCreate",
    "UserPreferenceRead",
    "UserPreferenceUpdate",
    "UserRead",
    "UserUpdate",
    "calendar_account_to_read",
    "calendar_event_to_read",
]
