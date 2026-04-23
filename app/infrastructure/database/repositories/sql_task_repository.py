from datetime import datetime

"""
Implementación SQL del repositorio de tareas.
Maneja la persistencia, filtrado y cálculo de completitud de tareas.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.domain.value_objects.task_priority import TaskPriority
from app.domain.value_objects.task_status import TaskStatus
from app.infrastructure.database.models.task_model import TaskModel


class SQLTaskRepository(TaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            priority=model.priority,
            task_list_id=model.task_list_id,
            assigned_user_id=model.assigned_user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create(self, task: Task) -> Task:
        model = TaskModel(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            task_list_id=task.task_list_id,
            assigned_user_id=task.assigned_user_id,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        return self._to_entity(model) if model else None

    def get_all_by_list(
        self,
        task_list_id: UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]:
        query = self.session.query(TaskModel).filter(
            TaskModel.task_list_id == task_list_id
        )
        if status:
            query = query.filter(TaskModel.status == status)
        if priority:
            query = query.filter(TaskModel.priority == priority)
        return [self._to_entity(m) for m in query.all()]

    def update(self, task: Task) -> Task:
        model = self.session.query(TaskModel).filter(TaskModel.id == task.id).first()
        model.title = task.title
        model.description = task.description
        model.status = task.status
        model.priority = task.priority
        model.assigned_user_id = task.assigned_user_id
        model.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def delete(self, task_id: UUID) -> None:
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        self.session.delete(model)
        self.session.commit()
