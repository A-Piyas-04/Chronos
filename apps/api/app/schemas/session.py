"""Scheduled work sessions."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import SessionSource, SessionStatus
from app.schemas.base import OrmSchema
from app.utils.time import ensure_utc


class ScheduledSessionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    task_id: UUID
    title_snapshot: str = Field(..., min_length=1, max_length=512)
    start_at: datetime
    end_at: datetime
    source: SessionSource = SessionSource.system_generated
    status: SessionStatus = SessionStatus.scheduled

    @model_validator(mode="after")
    def normalize_times_utc(self) -> ScheduledSessionCreate:
        start_at = ensure_utc(self.start_at)
        end_at = ensure_utc(self.end_at)
        if end_at <= start_at:
            raise ValueError("end_at must be after start_at")
        return self.model_copy(update={"start_at": start_at, "end_at": end_at})


class ScheduledSessionUpdate(BaseModel):
    title_snapshot: str | None = Field(default=None, min_length=1, max_length=512)
    start_at: datetime | None = None
    end_at: datetime | None = None
    status: SessionStatus | None = None

    @model_validator(mode="after")
    def normalize_times_utc(self) -> ScheduledSessionUpdate:
        updates: dict[str, datetime] = {}
        if self.start_at is not None:
            updates["start_at"] = ensure_utc(self.start_at)
        if self.end_at is not None:
            updates["end_at"] = ensure_utc(self.end_at)
        if not updates:
            return self
        return self.model_copy(update=updates)


class ScheduledSessionRead(OrmSchema):
    id: UUID
    user_id: UUID
    task_id: UUID
    title_snapshot: str
    start_at: datetime
    end_at: datetime
    source: SessionSource
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
