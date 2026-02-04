"""Unit tests for TodoManager service.

These tests validate the TodoManager's CRUD operations:
- Adding todos
- Retrieving todos (all, by ID, by category, by priority)
- Updating todos
- Deleting todos
- Marking todos complete/incomplete
- Counting todos
"""

import pytest
from src.services.todo_manager import TodoManager
from src.models.todo import Todo


class TestTodoManagerAdd:
    """Test TodoManager.add() method."""

    def test_add_todo_with_title_only(self):
        """Can add todo with just title."""
        manager = TodoManager()
        todo = manager.add("Buy milk")

        assert todo.id == 1
        assert todo.title == "Buy milk"
        assert todo.category is None
        assert todo.priority == "medium"
        assert todo.completed is False

    def test_add_todo_with_all_fields(self):
        """Can add todo with all fields specified."""
        manager = TodoManager()
        todo = manager.add("Write report", category="work", priority="high")

        assert todo.id == 1
        assert todo.title == "Write report"
        assert todo.category == "work"
        assert todo.priority == "high"

    def test_add_multiple_todos_increments_id(self):
        """Adding multiple todos auto-increments IDs."""
        manager = TodoManager()
        todo1 = manager.add("First task")
        todo2 = manager.add("Second task")
        todo3 = manager.add("Third task")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

    def test_add_invalid_title_raises_error(self):
        """Adding todo with empty title raises ValueError."""
        manager = TodoManager()
        with pytest.raises(ValueError, match="title cannot be empty"):
            manager.add("")

    def test_add_invalid_priority_raises_error(self):
        """Adding todo with invalid priority raises ValueError."""
        manager = TodoManager()
        with pytest.raises(ValueError, match="Priority must be"):
            manager.add("Task", priority="urgent")


class TestTodoManagerGetAll:
    """Test TodoManager.get_all() method."""

    def test_get_all_empty_list(self):
        """get_all() returns empty list when no todos exist."""
        manager = TodoManager()
        todos = manager.get_all()

        assert todos == []
        assert isinstance(todos, list)

    def test_get_all_returns_all_todos(self):
        """get_all() returns all added todos."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")
        manager.add("Task 3")

        todos = manager.get_all()

        assert len(todos) == 3
        assert todos[0].title == "Task 1"
        assert todos[1].title == "Task 2"
        assert todos[2].title == "Task 3"

    def test_get_all_returns_copy(self):
        """get_all() returns a copy, not the internal list."""
        manager = TodoManager()
        manager.add("Task 1")

        todos1 = manager.get_all()
        todos2 = manager.get_all()

        assert todos1 is not todos2
        assert todos1 == todos2


class TestTodoManagerGetById:
    """Test TodoManager.get_by_id() method."""

    def test_get_by_id_existing_todo(self):
        """get_by_id() returns todo with matching ID."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")
        manager.add("Task 3")

        todo = manager.get_by_id(2)

        assert todo is not None
        assert todo.id == 2
        assert todo.title == "Task 2"

    def test_get_by_id_nonexistent_todo(self):
        """get_by_id() returns None for non-existent ID."""
        manager = TodoManager()
        manager.add("Task 1")

        todo = manager.get_by_id(999)

        assert todo is None

    def test_get_by_id_empty_list(self):
        """get_by_id() returns None when no todos exist."""
        manager = TodoManager()
        todo = manager.get_by_id(1)

        assert todo is None


class TestTodoManagerUpdate:
    """Test TodoManager.update() method."""

    def test_update_todo_title(self):
        """Can update todo title."""
        manager = TodoManager()
        manager.add("Old title")

        updated = manager.update(1, title="New title")

        assert updated is not None
        assert updated.title == "New title"
        assert updated.id == 1

    def test_update_todo_category(self):
        """Can update todo category."""
        manager = TodoManager()
        manager.add("Task", category="work")

        updated = manager.update(1, category="personal")

        assert updated.category == "personal"

    def test_update_todo_priority(self):
        """Can update todo priority."""
        manager = TodoManager()
        manager.add("Task", priority="low")

        updated = manager.update(1, priority="high")

        assert updated.priority == "high"

    def test_update_multiple_fields(self):
        """Can update multiple fields at once."""
        manager = TodoManager()
        manager.add("Task", category="work", priority="low")

        updated = manager.update(1, title="Updated task", category="personal", priority="high")

        assert updated.title == "Updated task"
        assert updated.category == "personal"
        assert updated.priority == "high"

    def test_update_preserves_unchanged_fields(self):
        """Update preserves fields that aren't changed."""
        manager = TodoManager()
        original = manager.add("Task", category="work", priority="medium")

        updated = manager.update(1, title="New title")

        assert updated.title == "New title"
        assert updated.category == "work"
        assert updated.priority == "medium"
        assert updated.created_at == original.created_at

    def test_update_nonexistent_todo(self):
        """Updating non-existent todo returns None."""
        manager = TodoManager()
        updated = manager.update(999, title="New title")

        assert updated is None

    def test_update_with_invalid_priority(self):
        """Updating with invalid priority raises ValueError."""
        manager = TodoManager()
        manager.add("Task")

        with pytest.raises(ValueError, match="Priority must be"):
            manager.update(1, priority="urgent")

    def test_update_with_empty_title(self):
        """Updating with empty title raises ValueError."""
        manager = TodoManager()
        manager.add("Task")

        with pytest.raises(ValueError, match="title cannot be empty"):
            manager.update(1, title="")


class TestTodoManagerDelete:
    """Test TodoManager.delete() method."""

    def test_delete_existing_todo(self):
        """delete() removes todo and returns True."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")
        manager.add("Task 3")

        result = manager.delete(2)

        assert result is True
        assert manager.count() == 2
        assert manager.get_by_id(2) is None

    def test_delete_nonexistent_todo(self):
        """delete() returns False for non-existent ID."""
        manager = TodoManager()
        manager.add("Task 1")

        result = manager.delete(999)

        assert result is False
        assert manager.count() == 1

    def test_delete_from_empty_list(self):
        """delete() returns False when no todos exist."""
        manager = TodoManager()
        result = manager.delete(1)

        assert result is False


class TestTodoManagerMarkComplete:
    """Test TodoManager.mark_complete() method."""

    def test_mark_todo_complete(self):
        """mark_complete() sets completed to True."""
        manager = TodoManager()
        manager.add("Task")

        updated = manager.mark_complete(1, completed=True)

        assert updated is not None
        assert updated.completed is True

    def test_mark_todo_incomplete(self):
        """mark_complete() can set completed to False."""
        manager = TodoManager()
        todo = manager.add("Task")
        todo.completed = True

        updated = manager.mark_complete(1, completed=False)

        assert updated.completed is False

    def test_mark_complete_defaults_to_true(self):
        """mark_complete() defaults to True if not specified."""
        manager = TodoManager()
        manager.add("Task")

        updated = manager.mark_complete(1)

        assert updated.completed is True

    def test_mark_complete_nonexistent_todo(self):
        """mark_complete() returns None for non-existent ID."""
        manager = TodoManager()
        updated = manager.mark_complete(999)

        assert updated is None


class TestTodoManagerGetByCategory:
    """Test TodoManager.get_by_category() method."""

    def test_get_by_category_returns_matching_todos(self):
        """get_by_category() returns todos in specified category."""
        manager = TodoManager()
        manager.add("Task 1", category="work")
        manager.add("Task 2", category="personal")
        manager.add("Task 3", category="work")

        work_todos = manager.get_by_category("work")

        assert len(work_todos) == 2
        assert all(t.category == "work" for t in work_todos)

    def test_get_by_category_case_insensitive(self):
        """get_by_category() is case-insensitive."""
        manager = TodoManager()
        manager.add("Task 1", category="work")

        todos = manager.get_by_category("WORK")

        assert len(todos) == 1

    def test_get_by_category_no_matches(self):
        """get_by_category() returns empty list when no matches."""
        manager = TodoManager()
        manager.add("Task 1", category="work")

        todos = manager.get_by_category("personal")

        assert todos == []


class TestTodoManagerGetByPriority:
    """Test TodoManager.get_by_priority() method."""

    def test_get_by_priority_returns_matching_todos(self):
        """get_by_priority() returns todos with specified priority."""
        manager = TodoManager()
        manager.add("Task 1", priority="high")
        manager.add("Task 2", priority="low")
        manager.add("Task 3", priority="high")

        high_todos = manager.get_by_priority("high")

        assert len(high_todos) == 2
        assert all(t.priority == "high" for t in high_todos)

    def test_get_by_priority_case_insensitive(self):
        """get_by_priority() is case-insensitive."""
        manager = TodoManager()
        manager.add("Task 1", priority="high")

        todos = manager.get_by_priority("HIGH")

        assert len(todos) == 1

    def test_get_by_priority_no_matches(self):
        """get_by_priority() returns empty list when no matches."""
        manager = TodoManager()
        manager.add("Task 1", priority="medium")

        todos = manager.get_by_priority("low")

        assert todos == []


class TestTodoManagerCount:
    """Test TodoManager.count() and count_completed() methods."""

    def test_count_empty_list(self):
        """count() returns 0 when no todos exist."""
        manager = TodoManager()
        assert manager.count() == 0

    def test_count_returns_total(self):
        """count() returns total number of todos."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")
        manager.add("Task 3")

        assert manager.count() == 3

    def test_count_after_delete(self):
        """count() updates after deletion."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")
        manager.delete(1)

        assert manager.count() == 1

    def test_count_completed_empty_list(self):
        """count_completed() returns 0 when no todos exist."""
        manager = TodoManager()
        assert manager.count_completed() == 0

    def test_count_completed_none_completed(self):
        """count_completed() returns 0 when no todos are completed."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")

        assert manager.count_completed() == 0

    def test_count_completed_some_completed(self):
        """count_completed() returns count of completed todos."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")
        manager.add("Task 3")
        manager.mark_complete(1)
        manager.mark_complete(3)

        assert manager.count_completed() == 2
        assert manager.count() == 3

    def test_count_completed_all_completed(self):
        """count_completed() equals count() when all completed."""
        manager = TodoManager()
        manager.add("Task 1")
        manager.add("Task 2")
        manager.mark_complete(1)
        manager.mark_complete(2)

        assert manager.count_completed() == 2
        assert manager.count() == 2
