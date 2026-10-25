from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .repositories.tasks import TaskRepository


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    """Build the repository used by task endpoints.

    Tests replace this dependency with a mock repository, so they never need a
    database session.
    """
    return TaskRepository(db)
