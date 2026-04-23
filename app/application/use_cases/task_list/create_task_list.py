from typing import Optional
from uuid import UUID

"""
Caso de uso para crear una nueva lista de tareas.
"""

from app.domain.entities.task_list import TaskList
from app.domain.repositories.task_list_repository import TaskListRepository


class CreateTaskListUseCase:
    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(
        self, name: str, owner_id: UUID, description: Optional[str] = None
    ) -> TaskList:
        task_list = TaskList(name=name, owner_id=owner_id, description=description)
        return self.repository.create(task_list)
