"""User and user_preferences API types."""

from __future__ import annotations

from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.base import OrmSchema


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    image_url: str | None = Field(default=None, max_length=2048)
    google_sub: str | None = Field(default=None, max_length=255)


class UserUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=255)
    image_url: str | None = Field(default=None, max_length=2048)
    google_sub: str | None = Field(default=None, max_length=255)


class UserRead(OrmSchema):
    id: UUID
    email: str
    name: str
    image_url: str | None
    google_sub: str | None
    created_at: datetime
    updated_at: datetime


class UserPreferenceCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    timezone: str = Field(..., min_length=1, max_length=64)
    workday_start_time: time
    workday_end_time: time
    deep_work_start_time: time
    deep_work_end_time: time
    max_deep_work_block_minutes: int = Field(default=45, ge=15, le=180)


class UserPreferenceUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    timezone: str | None = Field(default=None, min_length=1, max_length=64)
    workday_start_time: time | None = None
    workday_end_time: time | None = None
    deep_work_start_time: time | None = None
    deep_work_end_time: time | None = None
    max_deep_work_block_minutes: int | None = Field(default=None, ge=15, le=180)


class UserPreferenceRead(OrmSchema):
    id: UUID
    user_id: UUID
    timezone: str
    workday_start_time: time
    workday_end_time: time
    deep_work_start_time: time
    deep_work_end_time: time
    max_deep_work_block_minutes: int
    created_at: datetime
    updated_at: datetime
