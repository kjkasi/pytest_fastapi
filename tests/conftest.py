from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import get_task_repository
from app.main import create_app
from app.repositories.tasks import TaskRepository


@pytest.fixture
def app() -> FastAPI:
    # The router test suite deliberately does not start the database lifespan.
    return create_app(initialize_database=False)


@pytest.fixture
def repository(app: FastAPI) -> Iterator[Mock]:
    repository_mock = Mock(spec=TaskRepository)
    app.dependency_overrides[get_task_repository] = lambda: repository_mock
    yield repository_mock
    app.dependency_overrides.clear()


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
