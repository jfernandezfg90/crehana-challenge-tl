"""
Router de Tareas.
Define los endpoints de la API para la gestión de tareas individuales,
incluyendo creación, actualización, eliminación y cambio de estado.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.api.v1.schemas.task_schemas import (
    TaskAssign,
    TaskCreate,
    TaskListWithCompletionResponse,
    TaskResponse,
    TaskStatusUpdate,
    TaskUpdate,
)
from app.application.use_cases.task.assign_task import AssignTaskUseCase
from app.application.use_cases.task.change_task_status import ChangeTaskStatusUseCase
from app.application.use_cases.task.create_task import CreateTaskUseCase
from app.application.use_cases.task.delete_task import DeleteTaskUseCase
from app.application.use_cases.task.get_task import GetTaskUseCase
from app.application.use_cases.task.list_tasks import ListTasksUseCase
from app.application.use_cases.task.update_task import UpdateTaskUseCase
from app.domain.entities.user import User
from app.domain.value_objects.task_priority import TaskPriority
from app.domain.value_objects.task_status import TaskStatus
from app.infrastructure.database.repositories.sql_task_list_repository import (
    SQLTaskListRepository,
)
from app.infrastructure.database.repositories.sql_task_repository import (
    SQLTaskRepository,
)
from app.infrastructure.database.repositories.sql_user_repository import (
    SQLUserRepository,
)
from app.infrastructure.notifications.fake_email_service import FakeEmailService

router = APIRouter(prefix="/task-lists/{list_id}/tasks", tags=["Tasks"])


def _to_response(task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        task_list_id=task.task_list_id,
        assigned_user_id=task.assigned_user_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    list_id: UUID,
    body: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = SQLTaskRepository(db)
    list_repo = SQLTaskListRepository(db)
    use_case = CreateTaskUseCase(task_repo, list_repo)
    task = use_case.execute(
        title=body.title,
        task_list_id=list_id,
        owner_id=current_user.id,
        description=body.description,
        priority=body.priority,
    )
    return _to_response(task)


@router.get("", response_model=TaskListWithCompletionResponse)
def list_tasks(
    list_id: UUID,
    status: TaskStatus = None,
    priority: TaskPriority = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = SQLTaskRepository(db)
    use_case = ListTasksUseCase(task_repo)
    result = use_case.execute(list_id, status=status, priority=priority)
    return TaskListWithCompletionResponse(
        tasks=[_to_response(t) for t in result.tasks],
        total=result.total,
        completion_percentage=result.completion_percentage,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    list_id: UUID,
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = SQLTaskRepository(db)
    use_case = GetTaskUseCase(task_repo)
    return _to_response(use_case.execute(task_id, list_id))


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    list_id: UUID,
    task_id: UUID,
    body: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = SQLTaskRepository(db)
    use_case = UpdateTaskUseCase(task_repo)
    task = use_case.execute(
        task_id=task_id,
        task_list_id=list_id,
        title=body.title,
        description=body.description,
        priority=body.priority,
    )
    return _to_response(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    list_id: UUID,
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = SQLTaskRepository(db)
    use_case = DeleteTaskUseCase(task_repo)
    use_case.execute(task_id, list_id)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def change_task_status(
    list_id: UUID,
    task_id: UUID,
    body: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = SQLTaskRepository(db)
    use_case = ChangeTaskStatusUseCase(task_repo)
    task = use_case.execute(task_id, list_id, body.status)
    return _to_response(task)


@router.patch("/{task_id}/assign", response_model=TaskResponse)
def assign_task(
    list_id: UUID,
    task_id: UUID,
    body: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = SQLTaskRepository(db)
    user_repo = SQLUserRepository(db)
    notification_svc = FakeEmailService()
    use_case = AssignTaskUseCase(task_repo, user_repo, notification_svc)
    task = use_case.execute(task_id, list_id, body.user_id)
    return _to_response(task)
