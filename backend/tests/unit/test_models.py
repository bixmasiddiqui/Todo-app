"""Unit tests for data models and schemas."""
import pytest
from pydantic import ValidationError
from src.models import Task
from src.schemas import TaskCreate, TaskUpdate, TaskResponse


class TestTaskModel:
    """Tests for Task SQLModel."""

    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(title="Test task")
        assert task.title == "Test task"
        assert task.completed is False
        assert task.description is None
        assert task.id is not None
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_with_completion(self):
        """Test creating a completed task."""
        task = Task(title="Completed task", completed=True)
        assert task.completed is True

    def test_task_with_description(self):
        """Test creating a task with description."""
        task = Task(title="My task", description="Some details")
        assert task.title == "My task"
        assert task.description == "Some details"


class TestTaskCreateSchema:
    """Tests for TaskCreate schema."""

    def test_valid_creation(self):
        """Test valid task creation schema."""
        data = {"title": "Buy groceries"}
        task_create = TaskCreate(**data)
        assert task_create.title == "Buy groceries"

    def test_title_trimming(self):
        """Test that title is trimmed."""
        data = {"title": "  Trimmed task  "}
        task_create = TaskCreate(**data)
        assert task_create.title == "Trimmed task"

    def test_empty_title_fails(self):
        """Test that empty title fails validation."""
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_whitespace_only_fails(self):
        """Test that whitespace-only title fails."""
        with pytest.raises(ValidationError):
            TaskCreate(title="   ")

    def test_max_length_validation(self):
        """Test that title exceeding 200 chars fails."""
        long_title = "a" * 201
        with pytest.raises(ValidationError):
            TaskCreate(title=long_title)

    def test_max_length_allowed(self):
        """Test that exactly 200 chars is allowed."""
        max_title = "a" * 200
        task_create = TaskCreate(title=max_title)
        assert len(task_create.title) == 200

    def test_optional_description(self):
        """Test that description is optional."""
        task_create = TaskCreate(title="Task")
        assert task_create.description is None

    def test_with_description(self):
        """Test creating with description."""
        task_create = TaskCreate(title="Task", description="Details here")
        assert task_create.description == "Details here"


class TestTaskUpdateSchema:
    """Tests for TaskUpdate schema."""

    def test_update_title(self):
        """Test updating title only."""
        task_update = TaskUpdate(title="Updated title")
        assert task_update.title == "Updated title"
        assert task_update.completed is None

    def test_update_completion(self):
        """Test updating completion status only."""
        task_update = TaskUpdate(completed=True)
        assert task_update.completed is True
        assert task_update.title is None

    def test_update_both_fields(self):
        """Test updating both fields."""
        task_update = TaskUpdate(
            title="Updated task",
            completed=True
        )
        assert task_update.title == "Updated task"
        assert task_update.completed is True

    def test_empty_update(self):
        """Test creating empty update (all fields None)."""
        task_update = TaskUpdate()
        assert task_update.title is None
        assert task_update.completed is None

    def test_title_trimming_on_update(self):
        """Test that title is trimmed on update."""
        task_update = TaskUpdate(title="  Trimmed  ")
        assert task_update.title == "Trimmed"

    def test_empty_title_update_fails(self):
        """Test that empty title update fails."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="")

    def test_update_too_long_fails(self):
        """Test that title exceeding 200 chars fails on update."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="a" * 201)


class TestTaskResponseSchema:
    """Tests for TaskResponse schema."""

    def test_response_from_model(self):
        """Test creating response from model."""
        task = Task(title="Test task")
        response = TaskResponse.model_validate(task)
        assert response.title == "Test task"
        assert response.completed is False
        assert response.id == task.id
        assert response.created_at == task.created_at
        assert response.updated_at == task.updated_at

    def test_response_all_fields_required(self):
        """Test that all fields are required in response."""
        with pytest.raises(ValidationError):
            TaskResponse(title="Test")  # Missing other fields
