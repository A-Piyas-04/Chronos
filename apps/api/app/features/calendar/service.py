from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.calendar.repository import (
    CalendarAccountRepository,
    CalendarEventRepository,
)
from app.models.calendar_account import CalendarAccount
from app.models.calendar_event import CalendarEvent


class CalendarAccountService:
    def __init__(self, session: Session) -> None:
        self._repo = CalendarAccountRepository(session)

    def get_account(self, account_id: UUID, user_id: UUID) -> CalendarAccount:
        row = self._repo.get_by_id(account_id)
        if row is None or row.user_id != user_id:
            raise NotFoundError("Calendar account not found")
        return row


class CalendarEventService:
    def __init__(self, session: Session) -> None:
        self._repo = CalendarEventRepository(session)

    def get_event(self, event_id: UUID, user_id: UUID) -> CalendarEvent:
        row = self._repo.get_by_id(event_id)
        if row is None or row.user_id != user_id:
            raise NotFoundError("Calendar event not found")
        return row

    def list_in_range(
        self,
        user_id: UUID,
        start_at: datetime,
        end_at: datetime,
    ) -> list[CalendarEvent]:
        return self._repo.list_for_user_between(user_id, start_at, end_at)
