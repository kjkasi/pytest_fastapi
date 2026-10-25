from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..dependencies import get_task_repository
from ..repositories.tasks import TaskRepository
from ..schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _task_not_found(task_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found",
    )


@router.get("", response_model=list[TaskRead])
def list_tasks(
    repository: TaskRepository = Depends(get_task_repository),
) -> list[TaskRead]:
    return repository.list()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskRead:
    task = repository.get(task_id)
    if task is None:
        raise _task_not_found(task_id)
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskRead:
    return repository.create(
        title=payload.title,
        description=payload.description,
        is_completed=payload.is_completed,
    )


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskRead:
    task = repository.update(task_id, payload.model_dump(exclude_unset=True))
    if task is None:
        raise _task_not_found(task_id)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    repository: TaskRepository = Depends(get_task_repository),
) -> Response:
    if not repository.delete(task_id):
        raise _task_not_found(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
