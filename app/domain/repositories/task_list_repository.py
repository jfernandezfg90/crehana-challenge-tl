"""
Interfaz para el repositorio de listas de tareas.
Define el contrato que deben seguir las implementaciones de persistencia.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.task_list import TaskList


class TaskListRepository(ABC):
    @abstractmethod
    def create(self, task_list: TaskList) -> TaskList:
        pass

    @abstractmethod
    def get_by_id(self, task_list_id: UUID) -> Optional[TaskList]:
        pass

    @abstractmethod
    def get_all_by_owner(self, owner_id: UUID) -> List[TaskList]:
        pass

    @abstractmethod
    def update(self, task_list: TaskList) -> TaskList:
        pass

    @abstractmethod
    def delete(self, task_list_id: UUID) -> None:
        pass
