from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.tasks.repository import TaskRepository
from app.models.task import Task


class TaskService:
    def __init__(self, session: Session) -> None:
        self._repo = TaskRepository(session)

    def get_task(self, task_id: UUID, user_id: UUID) -> Task:
        row = self._repo.get_by_id(task_id)
        if row is None or row.user_id != user_id:
            raise NotFoundError("Task not found")
        return row
