"""Unit tests for data models and schemas."""
import pytest
from pydantic import ValidationError
from src.models import Task
from src.schemas import TaskCreate, TaskUpdate, TaskResponse


class TestTaskModel:
    """Tests for Task SQLModel."""

    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(description="Test task")
        assert task.description == "Test task"
        assert task.is_completed is False
        assert task.id is not None
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_with_completion(self):
        """Test creating a completed task."""
        task = Task(description="Completed task", is_completed=True)
        assert task.is_completed is True

    # Note: SQLModel doesn't raise ValidationError for missing required fields
    # Validation is handled by Pydantic schemas (TaskCreate, TaskUpdate)


class TestTaskCreateSchema:
    """Tests for TaskCreate schema."""

    def test_valid_creation(self):
        """Test valid task creation schema."""
        data = {"description": "Buy groceries"}
        task_create = TaskCreate(**data)
        assert task_create.description == "Buy groceries"

    def test_description_trimming(self):
        """Test that description is trimmed."""
        data = {"description": "  Trimmed task  "}
        task_create = TaskCreate(**data)
        assert task_create.description == "Trimmed task"

    def test_empty_description_fails(self):
        """Test that empty description fails validation."""
        with pytest.raises(ValidationError):
            TaskCreate(description="")

    def test_whitespace_only_fails(self):
        """Test that whitespace-only description fails."""
        with pytest.raises(ValidationError):
            TaskCreate(description="   ")

    def test_max_length_validation(self):
        """Test that description exceeding 500 chars fails."""
        long_description = "a" * 501
        with pytest.raises(ValidationError):
            TaskCreate(description=long_description)

    def test_max_length_allowed(self):
        """Test that exactly 500 chars is allowed."""
        max_description = "a" * 500
        task_create = TaskCreate(description=max_description)
        assert len(task_create.description) == 500


class TestTaskUpdateSchema:
    """Tests for TaskUpdate schema."""

    def test_update_description(self):
        """Test updating description only."""
        task_update = TaskUpdate(description="Updated description")
        assert task_update.description == "Updated description"
        assert task_update.is_completed is None

    def test_update_completion(self):
        """Test updating completion status only."""
        task_update = TaskUpdate(is_completed=True)
        assert task_update.is_completed is True
        assert task_update.description is None

    def test_update_both_fields(self):
        """Test updating both fields."""
        task_update = TaskUpdate(
            description="Updated task",
            is_completed=True
        )
        assert task_update.description == "Updated task"
        assert task_update.is_completed is True

    def test_empty_update(self):
        """Test creating empty update (all fields None)."""
        task_update = TaskUpdate()
        assert task_update.description is None
        assert task_update.is_completed is None

    def test_description_trimming_on_update(self):
        """Test that description is trimmed on update."""
        task_update = TaskUpdate(description="  Trimmed  ")
        assert task_update.description == "Trimmed"

    def test_empty_description_update_fails(self):
        """Test that empty description update fails."""
        with pytest.raises(ValidationError):
            TaskUpdate(description="")

    def test_update_too_long_fails(self):
        """Test that description exceeding 500 chars fails on update."""
        with pytest.raises(ValidationError):
            TaskUpdate(description="a" * 501)


class TestTaskResponseSchema:
    """Tests for TaskResponse schema."""

    def test_response_from_model(self):
        """Test creating response from model."""
        task = Task(description="Test task")
        response = TaskResponse.model_validate(task)
        assert response.description == "Test task"
        assert response.is_completed is False
        assert response.id == task.id
        assert response.created_at == task.created_at
        assert response.updated_at == task.updated_at

    def test_response_all_fields_required(self):
        """Test that all fields are required in response."""
        with pytest.raises(ValidationError):
            TaskResponse(description="Test")  # Missing other fields
