from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.value_objects.task_priority import TaskPriority
from app.domain.value_objects.task_status import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskAssign(BaseModel):
    user_id: UUID


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    task_list_id: UUID
    assigned_user_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListWithCompletionResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    completion_percentage: float
