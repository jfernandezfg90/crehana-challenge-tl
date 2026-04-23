"""
Caso de uso para eliminar una lista de tareas.
Valida la existencia y pertenencia antes de borrar.
"""

from uuid import UUID

from app.domain.exceptions.domain_exceptions import (
    TaskListNotFoundException,
    UnauthorizedAccessException,
)
from app.domain.repositories.task_list_repository import TaskListRepository


class DeleteTaskListUseCase:
    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(self, task_list_id: UUID, owner_id: UUID) -> None:
        task_list = self.repository.get_by_id(task_list_id)
        if not task_list:
            raise TaskListNotFoundException(str(task_list_id))
        if task_list.owner_id != owner_id:
            raise UnauthorizedAccessException("task list")
        self.repository.delete(task_list_id)
