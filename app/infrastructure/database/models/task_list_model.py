"""
Modelo de base de datos para las listas de tareas.
Define la estructura de la tabla 'task_lists' y sus relaciones.
"""

import uuid

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.connection import Base


class TaskListModel(Base):
    __tablename__ = "task_lists"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    owner = relationship("UserModel", back_populates="task_lists")
    tasks = relationship(
        "TaskModel", back_populates="task_list", cascade="all, delete-orphan"
    )
