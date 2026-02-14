"""Database models using SQLModel."""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model for authentication."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, nullable=False, unique=True, index=True)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Task(SQLModel, table=True):
    """Task model representing a todo item."""

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000, nullable=True)
    completed: bool = Field(default=False, nullable=False)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
