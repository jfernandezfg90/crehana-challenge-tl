"""
Modelo de Base de Datos: Usuario.
Mapeo ORM (SQLAlchemy) para la tabla de usuarios.
"""

import uuid

from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    task_lists = relationship("TaskListModel", back_populates="owner")
    assigned_tasks = relationship(
        "TaskModel",
        foreign_keys="TaskModel.assigned_user_id",
        back_populates="assigned_user",
    )
