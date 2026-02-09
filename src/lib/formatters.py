"""Display formatting utilities."""

from typing import List
from src.models.todo import Todo


def format_todo_list(todos: List[Todo], show_empty_message: bool = True) -> str:
    """
    Format a list of todos for display.

    Args:
        todos: List of todos to format
        show_empty_message: Whether to show "No todos" message if list is empty

    Returns:
        Formatted string ready for display
    """
    if not todos:
        if show_empty_message:
            return "No todos yet. Add your first task!"
        return ""

    lines = []
    for todo in todos:
        # Format: [ID] [X/  ] Title | category | priority
        checkbox = "[X]" if todo.completed else "[ ]"

        # Truncate title if too long (max 40 chars for display)
        title_display = todo.title
        if len(title_display) > 40:
            title_display = title_display[:37] + "..."

        # Format category and priority
        category_display = todo.category if todo.category else "none"
        priority_display = todo.priority

        # Build the line
        line = f"[{todo.id}] {checkbox} {title_display:<40} | {category_display:<10} | {priority_display}"
        lines.append(line)

        # Add created timestamp on next line
        created_str = todo.created_at.strftime("%Y-%m-%d %H:%M")
        lines.append(f"    Created: {created_str}")
        lines.append("")  # Empty line between todos

    return "\n".join(lines)


def format_status_line(total: int, completed: int) -> str:
    """
    Format the status line showing todo counts.

    Args:
        total: Total number of todos
        completed: Number of completed todos

    Returns:
        Formatted status string
    """
    if total == 0:
        return "Status: No todos yet"

    pending = total - completed
    return f"Status: {total} todos | {completed} completed | {pending} pending"


def format_header(text: str, width: int = 64) -> str:
    """
    Format a section header with visual separator.

    Args:
        text: Header text
        width: Total width of the header

    Returns:
        Formatted header string
    """
    separator = "=" * width
    # Center the text
    padding = (width - len(text)) // 2
    centered_text = " " * padding + text

    return f"{separator}\n{centered_text}\n{separator}"


def format_welcome_banner() -> str:
    """
    Format the welcome banner for app startup.

    Returns:
        Welcome banner string
    """
    return """╔════════════════════════════════════════════════════════════════╗
║                   Todo Manager - Phase I                       ║
║             In-Memory Console Application                      ║
╚════════════════════════════════════════════════════════════════╝

⚠️  NOTE: All todos are stored in memory only.
   Data will be lost when you exit the application.

Press ENTER to continue..."""


def format_goodbye_message() -> str:
    """
    Format the goodbye message for app exit.

    Returns:
        Goodbye message string
    """
    return """
════════════════════════════════════════════════════════════════
                       GOODBYE!
════════════════════════════════════════════════════════════════

⚠️  Remember: All todos have been discarded (in-memory only).

Thank you for using Todo Manager!

════════════════════════════════════════════════════════════════
"""


def format_success(message: str) -> str:
    """Format a success message."""
    return f"✓ {message}"


def format_error(message: str) -> str:
    """Format an error message."""
    return f"✗ Error: {message}"


def format_info(message: str) -> str:
    """Format an informational message."""
    return f"ℹ️  {message}"
