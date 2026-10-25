from __future__ import annotations

from collections.abc import Mapping

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Task


class TaskRepository:
    """Persistence operations for tasks.

    The repository owns SQLAlchemy calls. Routers depend on this class instead of
    knowing how a task is stored.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[Task]:
        statement = select(Task).order_by(Task.id)
        return list(self.session.scalars(statement).all())

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def create(
        self,
        *,
        title: str,
        description: str | None,
        is_completed: bool = False,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            is_completed=is_completed,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task_id: int, values: Mapping[str, object]) -> Task | None:
        task = self.get(task_id)
        if task is None:
            return None

        for field, value in values.items():
            setattr(task, field, value)

        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get(task_id)
        if task is None:
            return False

        self.session.delete(task)
        self.session.commit()
        return True
