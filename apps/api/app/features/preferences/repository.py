from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_preference import UserPreference


class UserPreferenceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_for_user(self, user_id: UUID) -> UserPreference | None:
        stmt = select(UserPreference).where(UserPreference.user_id == user_id)
        return self._session.scalar(stmt)

    def add(self, row: UserPreference) -> UserPreference:
        self._session.add(row)
        return row
