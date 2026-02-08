"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Attributes:
        title: Task title (1-200 characters, trimmed)
        description: Optional task description (max 1000 characters)
    """

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('title')
    @classmethod
    def trim_and_validate_title(cls, v: str) -> str:
        """Trim whitespace and validate title."""
        trimmed = v.strip()
        if not trimmed:
            raise ValueError('Title cannot be empty or whitespace only')
        if len(trimmed) > 200:
            raise ValueError('Title must be 200 characters or less')
        return trimmed


class TaskUpdate(BaseModel):
    """Schema for updating a task.

    Attributes:
        title: Optional new title (1-200 characters, trimmed)
        description: Optional new description (max 1000 characters)
        completed: Optional new completion status
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def trim_and_validate_title(cls, v: str | None) -> str | None:
        """Trim whitespace and validate title."""
        if v is None:
            return None
        trimmed = v.strip()
        if not trimmed:
            raise ValueError('Title cannot be empty or whitespace only')
        if len(trimmed) > 200:
            raise ValueError('Title must be 200 characters or less')
        return trimmed


class TaskResponse(BaseModel):
    """Schema for task response.

    Attributes:
        id: Task UUID
        title: Task title
        description: Task description
        completed: Completion status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
