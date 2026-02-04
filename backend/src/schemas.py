"""Pydantic schemas for request/response validation."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Attributes:
        description: Task description (1-500 characters, trimmed)
    """

    description: str = Field(..., min_length=1, max_length=500)

    @field_validator('description')
    @classmethod
    def trim_and_validate_description(cls, v: str) -> str:
        """Trim whitespace and validate description."""
        trimmed = v.strip()
        if not trimmed:
            raise ValueError('Description cannot be empty or whitespace only')
        if len(trimmed) > 500:
            raise ValueError('Description must be 500 characters or less')
        return trimmed


class TaskUpdate(BaseModel):
    """Schema for updating a task.

    Attributes:
        description: Optional new description (1-500 characters, trimmed)
        is_completed: Optional new completion status
    """

    description: str | None = Field(None, min_length=1, max_length=500)
    is_completed: bool | None = None

    @field_validator('description')
    @classmethod
    def trim_and_validate_description(cls, v: str | None) -> str | None:
        """Trim whitespace and validate description."""
        if v is None:
            return None
        trimmed = v.strip()
        if not trimmed:
            raise ValueError('Description cannot be empty or whitespace only')
        if len(trimmed) > 500:
            raise ValueError('Description must be 500 characters or less')
        return trimmed


class TaskResponse(BaseModel):
    """Schema for task response.

    Attributes:
        id: Task UUID
        description: Task description
        is_completed: Completion status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
