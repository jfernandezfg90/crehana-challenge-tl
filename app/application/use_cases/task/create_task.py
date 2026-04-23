from typing import Optional
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.exceptions.domain_exceptions import TaskListNotFoundException
from app.domain.repositories.task_list_repository import TaskListRepository
from app.domain.repositories.task_repository import TaskRepository
from app.domain.value_objects.task_priority import TaskPriority


class CreateTaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        task_list_repository: TaskListRepository,
    ):
        self.task_repository = task_repository
        self.task_list_repository = task_list_repository

    def execute(
        self,
        title: str,
        task_list_id: UUID,
        owner_id: UUID,
        description: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> Task:
        task_list = self.task_list_repository.get_by_id(task_list_id)
        if not task_list or task_list.owner_id != owner_id:
            raise TaskListNotFoundException(str(task_list_id))

        task = Task(
            title=title,
            task_list_id=task_list_id,
            description=description,
            priority=priority,
        )
        return self.task_repository.create(task)
