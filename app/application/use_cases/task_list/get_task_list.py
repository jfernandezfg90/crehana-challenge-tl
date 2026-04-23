"""
Caso de uso para obtener las listas de tareas.
Permite recuperar una lista específica o todas las listas de un usuario.
"""

from typing import List
from uuid import UUID

from app.domain.entities.task_list import TaskList
from app.domain.exceptions.domain_exceptions import (
    TaskListNotFoundException,
    UnauthorizedAccessException,
)
from app.domain.repositories.task_list_repository import TaskListRepository


class GetTaskListUseCase:
    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(self, task_list_id: UUID, owner_id: UUID) -> TaskList:
        task_list = self.repository.get_by_id(task_list_id)
        if not task_list:
            raise TaskListNotFoundException(str(task_list_id))
        if task_list.owner_id != owner_id:
            raise UnauthorizedAccessException("task list")
        return task_list

    def execute_all(self, owner_id: UUID) -> List[TaskList]:
        return self.repository.get_all_by_owner(owner_id)
