"""Contract tests for Todo model.

These tests validate the Todo model's data contract:
- Required fields and their types
- Validation rules for all attributes
- Default values and auto-generated fields
"""

import pytest
from datetime import datetime
from src.models.todo import Todo


class TestTodoContract:
    """Test Todo model contract and validation."""

    def test_todo_creation_with_required_fields(self):
        """Todo can be created with just id and title."""
        todo = Todo(id=1, title="Test task")

        assert todo.id == 1
        assert todo.title == "Test task"
        assert todo.completed is False
        assert todo.category is None
        assert todo.priority == "medium"
        assert isinstance(todo.created_at, datetime)

    def test_todo_creation_with_all_fields(self):
        """Todo can be created with all fields specified."""
        created = datetime(2026, 1, 2, 10, 30)
        todo = Todo(
            id=5,
            title="Complete project",
            completed=True,
            category="work",
            priority="high",
            created_at=created
        )

        assert todo.id == 5
        assert todo.title == "Complete project"
        assert todo.completed is True
        assert todo.category == "work"
        assert todo.priority == "high"
        assert todo.created_at == created

    def test_todo_title_cannot_be_empty(self):
        """Todo creation fails when title is empty string."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Todo(id=1, title="")

    def test_todo_title_cannot_be_whitespace_only(self):
        """Todo creation fails when title is only whitespace."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Todo(id=1, title="   ")

    def test_todo_title_max_length(self):
        """Todo creation fails when title exceeds 500 characters."""
        long_title = "x" * 501
        with pytest.raises(ValueError, match="cannot exceed 500 characters"):
            Todo(id=1, title=long_title)

    def test_todo_title_accepts_max_valid_length(self):
        """Todo accepts title exactly at 500 character limit."""
        valid_title = "x" * 500
        todo = Todo(id=1, title=valid_title)
        assert len(todo.title) == 500

    def test_todo_priority_must_be_valid(self):
        """Todo creation fails with invalid priority."""
        with pytest.raises(ValueError, match="Priority must be high, medium, or low"):
            Todo(id=1, title="Test", priority="urgent")

    def test_todo_priority_accepts_high(self):
        """Todo accepts 'high' priority."""
        todo = Todo(id=1, title="Test", priority="high")
        assert todo.priority == "high"

    def test_todo_priority_accepts_medium(self):
        """Todo accepts 'medium' priority."""
        todo = Todo(id=1, title="Test", priority="medium")
        assert todo.priority == "medium"

    def test_todo_priority_accepts_low(self):
        """Todo accepts 'low' priority."""
        todo = Todo(id=1, title="Test", priority="low")
        assert todo.priority == "low"

    def test_todo_priority_case_insensitive(self):
        """Todo normalizes priority to lowercase."""
        todo = Todo(id=1, title="Test", priority="HIGH")
        assert todo.priority == "high"

    def test_todo_category_is_optional(self):
        """Todo can be created without category."""
        todo = Todo(id=1, title="Test")
        assert todo.category is None

    def test_todo_category_normalizes_to_lowercase(self):
        """Todo normalizes category to lowercase."""
        todo = Todo(id=1, title="Test", category="WORK")
        assert todo.category == "work"

    def test_todo_category_strips_whitespace(self):
        """Todo strips whitespace from category."""
        todo = Todo(id=1, title="Test", category="  personal  ")
        assert todo.category == "personal"

    def test_todo_category_empty_string_becomes_none(self):
        """Todo converts empty category to None."""
        todo = Todo(id=1, title="Test", category="")
        assert todo.category is None

    def test_todo_category_whitespace_only_becomes_none(self):
        """Todo converts whitespace-only category to None."""
        todo = Todo(id=1, title="Test", category="   ")
        assert todo.category is None

    def test_todo_category_max_length(self):
        """Todo creation fails when category exceeds 50 characters."""
        long_category = "x" * 51
        with pytest.raises(ValueError, match="Category cannot exceed 50 characters"):
            Todo(id=1, title="Test", category=long_category)

    def test_todo_category_accepts_max_valid_length(self):
        """Todo accepts category exactly at 50 character limit."""
        valid_category = "x" * 50
        todo = Todo(id=1, title="Test", category=valid_category)
        assert len(todo.category) == 50

    def test_todo_completed_defaults_to_false(self):
        """Todo completion status defaults to False."""
        todo = Todo(id=1, title="Test")
        assert todo.completed is False

    def test_todo_completed_can_be_set_to_true(self):
        """Todo can be created with completed=True."""
        todo = Todo(id=1, title="Test", completed=True)
        assert todo.completed is True

    def test_todo_created_at_auto_generated(self):
        """Todo auto-generates created_at timestamp."""
        before = datetime.now()
        todo = Todo(id=1, title="Test")
        after = datetime.now()

        assert before <= todo.created_at <= after

    def test_todo_to_dict_conversion(self):
        """Todo can be converted to dictionary."""
        todo = Todo(id=1, title="Test task", category="work", priority="high")
        data = todo.to_dict()

        assert data["id"] == 1
        assert data["title"] == "Test task"
        assert data["completed"] is False
        assert data["category"] == "work"
        assert data["priority"] == "high"
        assert isinstance(data["created_at"], str)

    def test_todo_from_dict_conversion(self):
        """Todo can be created from dictionary."""
        data = {
            "id": 2,
            "title": "From dict",
            "completed": True,
            "category": "personal",
            "priority": "low",
            "created_at": "2026-01-02T12:00:00"
        }

        todo = Todo.from_dict(data)

        assert todo.id == 2
        assert todo.title == "From dict"
        assert todo.completed is True
        assert todo.category == "personal"
        assert todo.priority == "low"
        assert isinstance(todo.created_at, datetime)

    def test_todo_roundtrip_dict_conversion(self):
        """Todo survives to_dict -> from_dict roundtrip."""
        original = Todo(id=3, title="Roundtrip test", category="test", priority="medium")
        data = original.to_dict()
        restored = Todo.from_dict(data)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.completed == original.completed
        assert restored.category == original.category
        assert restored.priority == original.priority
