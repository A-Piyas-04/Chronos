from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, task_id: UUID) -> Task | None:
        return self._session.get(Task, task_id)

    def list_for_user(self, user_id: UUID) -> list[Task]:
        stmt = select(Task).where(Task.user_id == user_id)
        return list(self._session.scalars(stmt).all())

    def add(self, row: Task) -> Task:
        self._session.add(row)
        return row
