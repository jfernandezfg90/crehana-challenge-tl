"""
Router de Listas de Tareas.
Provee endpoints para gestionar colecciones de tareas (Listas),
incluyendo su creación, consulta y eliminación.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.api.v1.schemas.task_list_schemas import (
    TaskListCreate,
    TaskListResponse,
    TaskListUpdate,
)
from app.application.use_cases.task_list.create_task_list import CreateTaskListUseCase
from app.application.use_cases.task_list.delete_task_list import DeleteTaskListUseCase
from app.application.use_cases.task_list.get_task_list import GetTaskListUseCase
from app.application.use_cases.task_list.update_task_list import UpdateTaskListUseCase
from app.domain.entities.user import User
from app.infrastructure.database.repositories.sql_task_list_repository import (
    SQLTaskListRepository,
)

router = APIRouter(prefix="/task-lists", tags=["Task Lists"])


def _to_response(tl) -> TaskListResponse:
    return TaskListResponse(
        id=tl.id,
        name=tl.name,
        description=tl.description,
        owner_id=tl.owner_id,
        created_at=tl.created_at,
        updated_at=tl.updated_at,
    )


@router.post("", response_model=TaskListResponse, status_code=status.HTTP_201_CREATED)
def create_task_list(
    body: TaskListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLTaskListRepository(db)
    use_case = CreateTaskListUseCase(repo)
    tl = use_case.execute(
        name=body.name, owner_id=current_user.id, description=body.description
    )
    return _to_response(tl)


@router.get("", response_model=List[TaskListResponse])
def list_task_lists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLTaskListRepository(db)
    use_case = GetTaskListUseCase(repo)
    return [_to_response(tl) for tl in use_case.execute_all(current_user.id)]


@router.get("/{list_id}", response_model=TaskListResponse)
def get_task_list(
    list_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLTaskListRepository(db)
    use_case = GetTaskListUseCase(repo)
    return _to_response(use_case.execute(list_id, current_user.id))


@router.put("/{list_id}", response_model=TaskListResponse)
def update_task_list(
    list_id: UUID,
    body: TaskListUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLTaskListRepository(db)
    use_case = UpdateTaskListUseCase(repo)
    tl = use_case.execute(
        task_list_id=list_id,
        owner_id=current_user.id,
        name=body.name,
        description=body.description,
    )
    return _to_response(tl)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_list(
    list_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLTaskListRepository(db)
    use_case = DeleteTaskListUseCase(repo)
    use_case.execute(task_list_id=list_id, owner_id=current_user.id)
