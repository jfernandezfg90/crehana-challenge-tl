from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class TaskList:
    name: str
    owner_id: UUID
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
