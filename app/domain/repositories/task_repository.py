"""
Interfaz para el repositorio de tareas.
Define el contrato para la gestión de tareas, filtros y métricas.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.value_objects.task_priority import TaskPriority
from app.domain.value_objects.task_status import TaskStatus


class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        pass

    @abstractmethod
    def get_all_by_list(
        self,
        task_list_id: UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        pass
