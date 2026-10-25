from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.models import Task
from app.repositories.tasks import TaskRepository


@pytest.fixture
def session() -> MagicMock:
    # No engine, connection, or SQLite file is created in these tests.
    return MagicMock(spec=Session)


@pytest.fixture
def repository(session: MagicMock) -> TaskRepository:
    return TaskRepository(session)


def test_list_uses_session_scalars_without_a_database(
    repository: TaskRepository,
    session: MagicMock,
) -> None:
    tasks = [Task(id=1, title="Read", description=None, is_completed=False)]
    session.scalars.return_value.all.return_value = tasks

    result = repository.list()

    assert result == tasks
    session.scalars.assert_called_once()
    session.scalars.return_value.all.assert_called_once_with()


def test_get_delegates_to_session_get(
    repository: TaskRepository,
    session: MagicMock,
) -> None:
    task = Task(id=7, title="Read", description=None, is_completed=False)
    session.get.return_value = task

    result = repository.get(7)

    assert result is task
    session.get.assert_called_once_with(Task, 7)


def test_create_adds_commits_and_refreshes(
    repository: TaskRepository,
    session: MagicMock,
) -> None:
    created = repository.create(
        title="Write tests",
        description="Use a mock session",
        is_completed=False,
    )

    assert created.title == "Write tests"
    assert created.description == "Use a mock session"
    session.add.assert_called_once_with(created)
    session.commit.assert_called_once_with()
    session.refresh.assert_called_once_with(created)


def test_update_changes_the_entity_and_persists_it(
    repository: TaskRepository,
    session: MagicMock,
) -> None:
    task = Task(id=3, title="Old title", description=None, is_completed=False)
    session.get.return_value = task

    result = repository.update(
        3,
        {"title": "New title", "is_completed": True},
    )

    assert result is task
    assert task.title == "New title"
    assert task.is_completed is True
    session.get.assert_called_once_with(Task, 3)
    session.commit.assert_called_once_with()
    session.refresh.assert_called_once_with(task)


def test_update_returns_none_for_a_missing_task(
    repository: TaskRepository,
    session: MagicMock,
) -> None:
    session.get.return_value = None

    assert repository.update(404, {"title": "Missing"}) is None
    session.commit.assert_not_called()
    session.refresh.assert_not_called()


def test_delete_removes_and_commits(
    repository: TaskRepository,
    session: MagicMock,
) -> None:
    task = Task(id=5, title="Delete me", description=None, is_completed=False)
    session.get.return_value = task

    assert repository.delete(5) is True

    session.get.assert_called_once_with(Task, 5)
    session.delete.assert_called_once_with(task)
    session.commit.assert_called_once_with()


def test_delete_returns_false_for_a_missing_task(
    repository: TaskRepository,
    session: MagicMock,
) -> None:
    session.get.return_value = None

    assert repository.delete(404) is False
    session.delete.assert_not_called()
    session.commit.assert_not_called()
