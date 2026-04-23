"""
Modelo de base de datos para las tareas.
Define la estructura de la tabla 'tasks', sus estados, prioridades y relaciones.
"""

import uuid

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.task_priority import TaskPriority
from app.domain.value_objects.task_status import TaskStatus
from app.infrastructure.database.connection import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, native_enum=False), nullable=False, default=TaskStatus.PENDING
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority, native_enum=False),
        nullable=False,
        default=TaskPriority.MEDIUM,
    )
    task_list_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("task_lists.id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    task_list = relationship("TaskListModel", back_populates="tasks")
    assigned_user = relationship(
        "UserModel",
        foreign_keys=[assigned_user_id],
        back_populates="assigned_tasks",
    )
