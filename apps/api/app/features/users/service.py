from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.users.repository import UserRepository
from app.models.user import User


class UserService:
    def __init__(self, session: Session) -> None:
        self._repo = UserRepository(session)

    def get_user(self, user_id: UUID) -> User:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user
