from typing import Optional
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.exceptions.domain_exceptions import TaskNotFoundException
from app.domain.repositories.task_repository import TaskRepository
from app.domain.value_objects.task_priority import TaskPriority


class UpdateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(
        self,
        task_id: UUID,
        task_list_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
    ) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task or task.task_list_id != task_list_id:
            raise TaskNotFoundException(str(task_id))

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority

        return self.task_repository.update(task)
