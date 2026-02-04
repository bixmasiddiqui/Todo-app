"""CLI command handlers for todo operations."""

from typing import Optional
from src.services.todo_manager import TodoManager
from src.cli.menu import get_todo_input, pause_for_user
from src.lib.validators import validate_title, validate_priority, validate_category
from src.lib.formatters import (
    format_success,
    format_error,
    format_todo_list,
    format_status_line,
    format_header,
)


def handle_add_todo(manager: TodoManager) -> None:
    """
    Handle the 'add todo' command.

    Prompts user for todo details, validates input, and adds to manager.

    Args:
        manager: The TodoManager instance to add the todo to
    """
    # Get input from user
    todo_data = get_todo_input()

    # Validate title
    is_valid, error = validate_title(todo_data["title"])
    if not is_valid:
        print("\n" + format_error(error))
        pause_for_user()
        return

    # Validate category
    is_valid, error = validate_category(todo_data["category"])
    if not is_valid:
        print("\n" + format_error(error))
        pause_for_user()
        return

    # Validate priority
    is_valid, error = validate_priority(todo_data["priority"])
    if not is_valid:
        print("\n" + format_error(error))
        pause_for_user()
        return

    # All valid - add the todo
    try:
        todo = manager.add(
            title=todo_data["title"],
            category=todo_data["category"],
            priority=todo_data["priority"],
        )

        # Show success message
        print("\n" + format_success(f"Todo added successfully! (ID: {todo.id})"))
        print(f"  Title: {todo.title}")
        if todo.category:
            print(f"  Category: {todo.category}")
        print(f"  Priority: {todo.priority}")

    except ValueError as e:
        print("\n" + format_error(str(e)))

    pause_for_user()


def handle_list_todos(manager: TodoManager) -> None:
    """
    Handle the 'list todos' command.

    Displays all todos in a formatted list with status line.

    Args:
        manager: The TodoManager instance to list todos from
    """
    print("\n" + format_header("YOUR TODOS"))

    # Get all todos
    todos = manager.get_all()

    # Display the list
    todo_output = format_todo_list(todos, show_empty_message=True)
    print("\n" + todo_output)

    # Display status line
    if todos:
        status = format_status_line(manager.count(), manager.count_completed())
        print("\n" + "=" * 64)
        print(status)
        print("=" * 64)

    pause_for_user()


def handle_exit() -> None:
    """
    Handle the 'exit' command.

    Displays goodbye message.
    """
    from src.lib.formatters import format_goodbye_message

    print("\n" + format_goodbye_message())
