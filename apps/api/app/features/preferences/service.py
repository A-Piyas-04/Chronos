from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.preferences.repository import UserPreferenceRepository
from app.models.user_preference import UserPreference


class UserPreferenceService:
    def __init__(self, session: Session) -> None:
        self._repo = UserPreferenceRepository(session)

    def get_for_user(self, user_id: UUID) -> UserPreference:
        row = self._repo.get_for_user(user_id)
        if row is None:
            raise NotFoundError("User preferences not found")
        return row
