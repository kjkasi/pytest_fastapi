from __future__ import annotations

from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.models import Task
from app.repositories.tasks import TaskRepository


def make_task(**overrides: object) -> Task:
    values: dict[str, object] = {
        "id": 1,
        "title": "Buy milk",
        "description": "Remember the milk",
        "is_completed": False,
    }
    values.update(overrides)
    return Task(**values)


def test_list_tasks_uses_the_mocked_repository(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.list.return_value = [make_task()]

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Buy milk",
            "description": "Remember the milk",
            "is_completed": False,
        }
    ]
    repository.list.assert_called_once_with()


def test_get_task_returns_the_repository_result(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.get.return_value = make_task()

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"
    repository.get.assert_called_once_with(1)


def test_get_task_returns_404_when_repository_returns_none(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.get.return_value = None

    response = client.get("/tasks/404")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task 404 not found"}


def test_create_task_passes_payload_to_the_repository(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.create.return_value = make_task()

    response = client.post(
        "/tasks",
        json={
            "title": "Buy milk",
            "description": "Remember the milk",
            "is_completed": False,
        },
    )

    assert response.status_code == 201
    repository.create.assert_called_once_with(
        title="Buy milk",
        description="Remember the milk",
        is_completed=False,
    )


def test_update_task_passes_only_sent_fields_to_the_repository(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.update.return_value = make_task(title="Buy coffee", is_completed=True)

    response = client.patch(
        "/tasks/1",
        json={"title": "Buy coffee", "is_completed": True},
    )

    assert response.status_code == 200
    repository.update.assert_called_once_with(
        1,
        {"title": "Buy coffee", "is_completed": True},
    )


def test_update_task_returns_404_when_repository_returns_none(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.update.return_value = None

    response = client.patch("/tasks/404", json={"title": "Missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Task 404 not found"}


def test_delete_task_returns_no_content(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.delete.return_value = True

    response = client.delete("/tasks/1")

    assert response.status_code == 204
    assert response.content == b""
    repository.delete.assert_called_once_with(1)


def test_delete_task_returns_404_when_repository_returns_false(
    client: TestClient,
    repository: Mock,
) -> None:
    repository.delete.return_value = False

    response = client.delete("/tasks/404")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task 404 not found"}
