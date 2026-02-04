"""Integration tests for User Story 1: Add and View Todos.

These tests validate the complete add/view workflow:
- Adding todos through the manager
- Viewing all todos
- Viewing empty state
- Multiple todo management
- End-to-end scenarios from spec
"""

import pytest
from src.services.todo_manager import TodoManager
from src.lib.formatters import format_todo_list, format_status_line
from src.lib.validators import validate_title, validate_priority, validate_category


class TestAddViewIntegration:
    """Integration tests for add and view workflow."""

    def test_add_first_todo_complete_flow(self):
        """Complete flow: validate input -> add todo -> view result."""
        manager = TodoManager()

        # Step 1: Validate input
        title = "Buy groceries"
        is_valid, error = validate_title(title)
        assert is_valid is True

        # Step 2: Add todo
        todo = manager.add(title)
        assert todo.id == 1
        assert todo.title == "Buy groceries"

        # Step 3: View result
        todos = manager.get_all()
        assert len(todos) == 1
        assert todos[0].title == "Buy groceries"

        # Step 4: Format for display
        output = format_todo_list(todos)
        assert "Buy groceries" in output
        assert "[1]" in output
        assert "[ ]" in output  # Not completed

    def test_add_multiple_todos_complete_flow(self):
        """Complete flow: add multiple todos and view list."""
        manager = TodoManager()

        # Add multiple todos
        todo1 = manager.add("Buy groceries", category="personal", priority="high")
        todo2 = manager.add("Finish report", category="work", priority="medium")
        todo3 = manager.add("Call dentist", priority="low")

        # Verify all added
        todos = manager.get_all()
        assert len(todos) == 3

        # Verify order (oldest first)
        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3

        # Verify content
        assert todos[0].title == "Buy groceries"
        assert todos[1].title == "Finish report"
        assert todos[2].title == "Call dentist"

        # Verify categories
        assert todos[0].category == "personal"
        assert todos[1].category == "work"
        assert todos[2].category is None

        # Verify priorities
        assert todos[0].priority == "high"
        assert todos[1].priority == "medium"
        assert todos[2].priority == "low"

    def test_view_empty_todo_list(self):
        """Viewing empty list shows appropriate message."""
        manager = TodoManager()

        todos = manager.get_all()
        assert todos == []

        # Format for display
        output = format_todo_list(todos, show_empty_message=True)
        assert "No todos yet" in output

    def test_status_line_updates_after_adding(self):
        """Status line accurately reflects todo counts."""
        manager = TodoManager()

        # Initially empty
        status = format_status_line(manager.count(), manager.count_completed())
        assert "No todos yet" in status

        # After adding one
        manager.add("Task 1")
        status = format_status_line(manager.count(), manager.count_completed())
        assert "1 todos" in status or "1 todo" in status
        assert "0 completed" in status
        assert "1 pending" in status

        # After adding more
        manager.add("Task 2")
        manager.add("Task 3")
        status = format_status_line(manager.count(), manager.count_completed())
        assert "3 todos" in status
        assert "0 completed" in status
        assert "3 pending" in status

    def test_input_validation_before_adding(self):
        """Integration: validate all inputs before adding todo."""
        manager = TodoManager()

        # Test scenario: user wants to add todo with all fields
        title = "Important meeting"
        category = "work"
        priority = "high"

        # Validate all inputs
        title_valid, title_error = validate_title(title)
        category_valid, category_error = validate_category(category)
        priority_valid, priority_error = validate_priority(priority)

        assert title_valid is True
        assert category_valid is True
        assert priority_valid is True

        # All valid, proceed with adding
        todo = manager.add(title, category=category, priority=priority)

        assert todo.title == "Important meeting"
        assert todo.category == "work"
        assert todo.priority == "high"

    def test_input_validation_rejects_invalid_todo(self):
        """Integration: validation prevents invalid todo from being added."""
        manager = TodoManager()

        # Test scenario: user provides invalid inputs
        invalid_title = ""
        invalid_priority = "urgent"

        # Validate inputs
        title_valid, title_error = validate_title(invalid_title)
        priority_valid, priority_error = validate_priority(invalid_priority)

        assert title_valid is False
        assert priority_valid is False

        # Don't add todo if validation fails
        initial_count = manager.count()
        assert initial_count == 0

    def test_scenario_from_spec_basic_usage(self):
        """Test scenario from spec: Alice adds and views todos."""
        manager = TodoManager()

        # Alice opens the app and sees empty state
        assert manager.count() == 0

        # Alice adds her first todo
        todo1 = manager.add("Buy birthday gift for mom", category="personal", priority="high")
        assert todo1.id == 1

        # Alice adds more todos
        todo2 = manager.add("Prepare presentation", category="work", priority="high")
        todo3 = manager.add("Book dentist appointment", category="personal", priority="medium")

        # Alice views all her todos
        todos = manager.get_all()
        assert len(todos) == 3

        # Verify display shows all required info
        output = format_todo_list(todos)
        assert "Buy birthday gift for mom" in output
        assert "Prepare presentation" in output
        assert "Book dentist appointment" in output
        assert "personal" in output
        assert "work" in output
        assert "high" in output
        assert "medium" in output

    def test_scenario_category_grouping(self):
        """Test scenario: user views todos by category."""
        manager = TodoManager()

        # Add todos in different categories
        manager.add("Team meeting", category="work", priority="high")
        manager.add("Buy groceries", category="personal", priority="medium")
        manager.add("Code review", category="work", priority="medium")
        manager.add("Gym session", category="personal", priority="low")
        manager.add("Update documentation", category="work", priority="low")

        # View all work todos
        work_todos = manager.get_by_category("work")
        assert len(work_todos) == 3
        assert all(t.category == "work" for t in work_todos)

        # View all personal todos
        personal_todos = manager.get_by_category("personal")
        assert len(personal_todos) == 2
        assert all(t.category == "personal" for t in personal_todos)

    def test_scenario_priority_filtering(self):
        """Test scenario: user views todos by priority."""
        manager = TodoManager()

        # Add todos with different priorities
        manager.add("Critical bug fix", priority="high")
        manager.add("Write tests", priority="medium")
        manager.add("Update README", priority="low")
        manager.add("Security patch", priority="high")
        manager.add("Refactor code", priority="medium")

        # View high priority todos
        high_priority = manager.get_by_priority("high")
        assert len(high_priority) == 2
        assert all(t.priority == "high" for t in high_priority)

        # View medium priority todos
        medium_priority = manager.get_by_priority("medium")
        assert len(medium_priority) == 2

        # View low priority todos
        low_priority = manager.get_by_priority("low")
        assert len(low_priority) == 1

    def test_edge_case_very_long_title_display(self):
        """Edge case: very long title is truncated in display."""
        manager = TodoManager()

        # Add todo with long title (but within limit)
        long_title = "This is a very long todo title that exceeds the display width but is still within the 500 character limit for storage"
        todo = manager.add(long_title)

        # Verify stored correctly
        assert todo.title == long_title
        assert len(todo.title) > 40  # Exceeds display width

        # Verify display truncates
        todos = manager.get_all()
        output = format_todo_list(todos)

        # Display should show truncated version
        assert "..." in output  # Truncation indicator

    def test_edge_case_unicode_characters(self):
        """Edge case: todos with unicode characters."""
        manager = TodoManager()

        # Add todos with unicode
        todo1 = manager.add("Buy 🍎 and 🍌 from store")
        todo2 = manager.add("Read 'War and Peace' by Толстой")
        todo3 = manager.add("Learn 日本語 basics")

        # Verify storage
        todos = manager.get_all()
        assert len(todos) == 3

        # Verify display
        output = format_todo_list(todos)
        assert "🍎" in output
        assert "🍌" in output
        assert "Толстой" in output
        assert "日本語" in output

    def test_complete_user_journey_first_session(self):
        """Complete user journey: first time using the app."""
        manager = TodoManager()

        # User starts with empty state
        assert manager.count() == 0
        empty_output = format_todo_list(manager.get_all())
        assert "No todos yet" in empty_output

        # User adds their first todo
        first_todo = manager.add("Learn Python", category="learning", priority="medium")
        assert first_todo.id == 1
        assert manager.count() == 1

        # User views their todo
        todos = manager.get_all()
        assert len(todos) == 1
        assert todos[0].title == "Learn Python"

        # User adds more todos
        manager.add("Build a project", category="learning", priority="high")
        manager.add("Practice coding", category="learning", priority="medium")
        manager.add("Read documentation", category="learning", priority="low")

        # User views full list
        all_todos = manager.get_all()
        assert len(all_todos) == 4

        # User checks status
        status = format_status_line(manager.count(), manager.count_completed())
        assert "4 todos" in status
        assert "0 completed" in status
        assert "4 pending" in status

        # Verify all todos are visible
        output = format_todo_list(all_todos)
        assert "Learn Python" in output
        assert "Build a project" in output
        assert "Practice coding" in output
        assert "Read documentation" in output
