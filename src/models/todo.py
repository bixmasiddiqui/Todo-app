"""Todo data model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-assigned by TodoManager)
        title: Task description (required, non-empty)
        completed: Completion status (default False)
        category: Optional grouping label
        priority: Priority level (high/medium/low, default medium)
        created_at: Creation timestamp (auto-set)
    """

    id: int
    title: str
    completed: bool = False
    category: Optional[str] = None
    priority: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate todo attributes after initialization."""
        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Todo title cannot be empty")
        if len(self.title) > 500:
            raise ValueError("Todo title cannot exceed 500 characters")

        # Validate priority
        if self.priority.lower() not in ["high", "medium", "low"]:
            raise ValueError(
                f"Priority must be high, medium, or low (got '{self.priority}')"
            )
        self.priority = self.priority.lower()

        # Normalize category
        if self.category is not None:
            self.category = self.category.strip()
            if not self.category:
                self.category = None
            elif len(self.category) > 50:
                raise ValueError("Category cannot exceed 50 characters")
            else:
                self.category = self.category.lower()

    def to_dict(self) -> dict:
        """Convert todo to dictionary for serialization (future use)."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "category": self.category,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Create todo from dictionary (future use for Phase II persistence)."""
        data_copy = data.copy()
        if "created_at" in data_copy and isinstance(data_copy["created_at"], str):
            data_copy["created_at"] = datetime.fromisoformat(data_copy["created_at"])
        return cls(**data_copy)
