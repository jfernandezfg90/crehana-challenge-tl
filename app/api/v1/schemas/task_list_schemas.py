from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TaskListCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TaskListUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TaskListResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
