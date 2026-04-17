"""Task inbox schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import TaskPriority, TaskStatus, TaskType
from app.schemas.base import OrmSchema
from app.utils.time import ensure_utc


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=512)
    estimated_duration_minutes: int = Field(..., ge=1, le=24 * 60)
    remaining_duration_minutes: int | None = Field(default=None, ge=0, le=24 * 60)
    deadline_at: datetime
    priority: TaskPriority
    task_type: TaskType | None = None
    status: TaskStatus = TaskStatus.inbox

    @model_validator(mode="after")
    def validate_task_create(self) -> TaskCreate:
        deadline_at = ensure_utc(self.deadline_at)
        remaining = (
            self.estimated_duration_minutes
            if self.remaining_duration_minutes is None
            else self.remaining_duration_minutes
        )
        if remaining > self.estimated_duration_minutes:
            raise ValueError("remaining_duration_minutes cannot exceed estimated_duration_minutes")
        return self.model_copy(
            update={
                "deadline_at": deadline_at,
                "remaining_duration_minutes": remaining,
            },
        )


class TaskUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=512)
    estimated_duration_minutes: int | None = Field(default=None, ge=1, le=24 * 60)
    remaining_duration_minutes: int | None = Field(default=None, ge=0, le=24 * 60)
    deadline_at: datetime | None = None
    priority: TaskPriority | None = None
    task_type: TaskType | None = None
    status: TaskStatus | None = None

    @model_validator(mode="after")
    def normalize_deadline_utc(self) -> TaskUpdate:
        if self.deadline_at is None:
            return self
        return self.model_copy(update={"deadline_at": ensure_utc(self.deadline_at)})


class TaskRead(OrmSchema):
    id: UUID
    user_id: UUID
    title: str
    estimated_duration_minutes: int
    remaining_duration_minutes: int
    deadline_at: datetime
    priority: TaskPriority
    task_type: TaskType | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
