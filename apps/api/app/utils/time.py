from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo


def utc_now() -> datetime:
    return datetime.now(UTC)


def to_user_timezone(value: datetime, tz_name: str) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(ZoneInfo(tz_name))
