"""
Entidad de Dominio: Tarea.
Representa una tarea individual con sus atributos y lógica de negocio.
Parte del núcleo del dominio, independiente de la base de datos.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.domain.value_objects.task_priority import TaskPriority
from app.domain.value_objects.task_status import TaskStatus


@dataclass
class Task:
    title: str
    task_list_id: UUID
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_user_id: Optional[UUID] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
