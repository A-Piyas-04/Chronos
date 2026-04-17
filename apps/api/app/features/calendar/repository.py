from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.calendar_account import CalendarAccount
from app.models.calendar_event import CalendarEvent


class CalendarAccountRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, account_id: UUID) -> CalendarAccount | None:
        return self._session.get(CalendarAccount, account_id)

    def list_for_user(self, user_id: UUID) -> list[CalendarAccount]:
        stmt = select(CalendarAccount).where(CalendarAccount.user_id == user_id)
        return list(self._session.scalars(stmt).all())

    def add(self, row: CalendarAccount) -> CalendarAccount:
        self._session.add(row)
        return row


class CalendarEventRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, event_id: UUID) -> CalendarEvent | None:
        return self._session.get(CalendarEvent, event_id)

    def list_for_user_between(
        self,
        user_id: UUID,
        start_at: datetime,
        end_at: datetime,
    ) -> list[CalendarEvent]:
        stmt = (
            select(CalendarEvent)
            .where(CalendarEvent.user_id == user_id)
            .where(CalendarEvent.start_at < end_at)
            .where(CalendarEvent.end_at > start_at)
        )
        return list(self._session.scalars(stmt).all())

    def add(self, row: CalendarEvent) -> CalendarEvent:
        self._session.add(row)
        return row
