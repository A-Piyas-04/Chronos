"""Domain enums mirrored in PostgreSQL via SQLAlchemy."""

from __future__ import annotations

import enum


class CalendarProvider(enum.StrEnum):
    google = "google"


class TaskPriority(enum.StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskType(enum.StrEnum):
    deep = "deep"
    mechanical = "mechanical"


class TaskStatus(enum.StrEnum):
    inbox = "inbox"
    scheduled = "scheduled"
    done = "done"


class SessionSource(enum.StrEnum):
    system_generated = "system_generated"
    user_manual = "user_manual"


class SessionStatus(enum.StrEnum):
    scheduled = "scheduled"
    completed = "completed"
    missed = "missed"
    cancelled = "cancelled"
