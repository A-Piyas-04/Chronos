from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.scheduling.repository import ScheduledSessionRepository
from app.models.scheduled_session import ScheduledSession


class ScheduledSessionService:
    def __init__(self, session: Session) -> None:
        self._repo = ScheduledSessionRepository(session)

    def get_session(self, session_id: UUID, user_id: UUID) -> ScheduledSession:
        row = self._repo.get_by_id(session_id)
        if row is None or row.user_id != user_id:
            raise NotFoundError("Scheduled session not found")
        return row

    def list_in_range(
        self,
        user_id: UUID,
        start_at: datetime,
        end_at: datetime,
    ) -> list[ScheduledSession]:
        return self._repo.list_for_user_between(user_id, start_at, end_at)
