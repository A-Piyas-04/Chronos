from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scheduled_session import ScheduledSession


class ScheduledSessionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, session_id: UUID) -> ScheduledSession | None:
        return self._session.get(ScheduledSession, session_id)

    def list_for_user_between(
        self,
        user_id: UUID,
        start_at: datetime,
        end_at: datetime,
    ) -> list[ScheduledSession]:
        stmt = (
            select(ScheduledSession)
            .where(ScheduledSession.user_id == user_id)
            .where(ScheduledSession.start_at < end_at)
            .where(ScheduledSession.end_at > start_at)
        )
        return list(self._session.scalars(stmt).all())

    def add(self, row: ScheduledSession) -> ScheduledSession:
        self._session.add(row)
        return row
