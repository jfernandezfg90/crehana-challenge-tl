from datetime import datetime

"""
Implementación SQL del repositorio de listas de tareas.
Utiliza SQLAlchemy para persistir y recuperar listas de tareas.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.entities.task_list import TaskList
from app.domain.repositories.task_list_repository import TaskListRepository
from app.infrastructure.database.models.task_list_model import TaskListModel


class SQLTaskListRepository(TaskListRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: TaskListModel) -> TaskList:
        return TaskList(
            id=model.id,
            name=model.name,
            description=model.description,
            owner_id=model.owner_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create(self, task_list: TaskList) -> TaskList:
        model = TaskListModel(
            id=task_list.id,
            name=task_list.name,
            description=task_list.description,
            owner_id=task_list.owner_id,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, task_list_id: UUID) -> Optional[TaskList]:
        model = (
            self.session.query(TaskListModel)
            .filter(TaskListModel.id == task_list_id)
            .first()
        )
        return self._to_entity(model) if model else None

    def get_all_by_owner(self, owner_id: UUID) -> List[TaskList]:
        models = (
            self.session.query(TaskListModel)
            .filter(TaskListModel.owner_id == owner_id)
            .all()
        )
        return [self._to_entity(m) for m in models]

    def update(self, task_list: TaskList) -> TaskList:
        model = (
            self.session.query(TaskListModel)
            .filter(TaskListModel.id == task_list.id)
            .first()
        )
        model.name = task_list.name
        model.description = task_list.description
        model.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def delete(self, task_list_id: UUID) -> None:
        model = (
            self.session.query(TaskListModel)
            .filter(TaskListModel.id == task_list_id)
            .first()
        )
        self.session.delete(model)
        self.session.commit()
