"""
Caso de uso para actualizar una lista de tareas.
"""

from typing import Optional
from uuid import UUID

from app.domain.entities.task_list import TaskList
from app.domain.exceptions.domain_exceptions import (
    TaskListNotFoundException,
    UnauthorizedAccessException,
)
from app.domain.repositories.task_list_repository import TaskListRepository


class UpdateTaskListUseCase:
    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(
        self,
        task_list_id: UUID,
        owner_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> TaskList:
        task_list = self.repository.get_by_id(task_list_id)
        if not task_list:
            raise TaskListNotFoundException(str(task_list_id))
        if task_list.owner_id != owner_id:
            raise UnauthorizedAccessException("task list")

        if name is not None:
            task_list.name = name
        if description is not None:
            task_list.description = description

        return self.repository.update(task_list)
