"""Calendar accounts and imported events."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.calendar_account import CalendarAccount
from app.models.calendar_event import CalendarEvent
from app.models.enums import CalendarProvider
from app.schemas.base import OrmSchema


class CalendarAccountCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    provider: CalendarProvider
    provider_account_id: str = Field(..., min_length=1, max_length=512)
    email: EmailStr
    access_token: str | None = None
    refresh_token: str | None = None
    token_expires_at: datetime | None = None


class CalendarAccountUpdate(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    token_expires_at: datetime | None = None


class CalendarAccountRead(OrmSchema):
    id: UUID
    user_id: UUID
    provider: CalendarProvider
    provider_account_id: str
    email: str
    token_expires_at: datetime | None
    has_access_token: bool
    has_refresh_token: bool
    created_at: datetime
    updated_at: datetime


def calendar_account_to_read(account: CalendarAccount) -> CalendarAccountRead:
    """Map ORM account to API shape without exposing token material."""
    return CalendarAccountRead(
        id=account.id,
        user_id=account.user_id,
        provider=account.provider,
        provider_account_id=account.provider_account_id,
        email=account.email,
        token_expires_at=account.token_expires_at,
        has_access_token=account.access_token is not None,
        has_refresh_token=account.refresh_token is not None,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


class CalendarEventCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    external_event_id: str = Field(..., min_length=1, max_length=1024)
    source_calendar_id: str | None = Field(default=None, max_length=512)
    title: str = Field(default="", max_length=65535)
    start_at: datetime
    end_at: datetime
    is_all_day: bool = False
    is_busy: bool = True
    raw_status: str | None = Field(default=None, max_length=64)
    calendar_account_id: UUID | None = None


class CalendarEventUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=65535)
    start_at: datetime | None = None
    end_at: datetime | None = None
    is_all_day: bool | None = None
    is_busy: bool | None = None
    raw_status: str | None = Field(default=None, max_length=64)
    last_synced_at: datetime | None = None


class CalendarEventRead(OrmSchema):
    id: UUID
    user_id: UUID
    calendar_account_id: UUID | None
    external_event_id: str
    source_calendar_id: str | None
    title: str
    start_at: datetime
    end_at: datetime
    is_all_day: bool
    is_busy: bool
    raw_status: str | None
    last_synced_at: datetime | None
    created_at: datetime
    updated_at: datetime


def calendar_event_to_read(event: CalendarEvent) -> CalendarEventRead:
    return CalendarEventRead.model_validate(event)
