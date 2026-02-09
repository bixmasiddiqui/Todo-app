"""Event type definitions for Kafka messages."""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class TaskEvent(BaseModel):
    """Schema for task lifecycle events published to Kafka."""
    event_type: str  # task.created | task.updated | task.deleted
    task_id: UUID
    timestamp: datetime
    data: Dict[str, Any]


class TaskCreatedData(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdatedData(BaseModel):
    changes: Dict[str, Any]


class TaskDeletedData(BaseModel):
    pass
