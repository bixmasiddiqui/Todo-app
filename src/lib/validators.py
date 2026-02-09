"""Input validation utilities."""

from typing import Tuple


def validate_title(title: str) -> Tuple[bool, str]:
    """
    Validate a todo title.

    Args:
        title: The title to validate

    Returns:
        Tuple of (is_valid, error_message)
        If valid: (True, "")
        If invalid: (False, "Error description")
    """
    if not title or not title.strip():
        return (False, "Todo title cannot be empty")

    if len(title) > 500:
        return (False, "Title too long (max 500 characters)")

    return (True, "")


def validate_priority(priority: str) -> Tuple[bool, str]:
    """
    Validate a priority level.

    Args:
        priority: The priority to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not priority:
        # Empty is OK, will default to "medium"
        return (True, "")

    if priority.lower() not in ["high", "medium", "low"]:
        return (False, "Priority must be high, medium, or low")

    return (True, "")


def validate_category(category: str) -> Tuple[bool, str]:
    """
    Validate a category.

    Args:
        category: The category to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not category:
        # Empty is OK (optional field)
        return (True, "")

    if len(category) > 50:
        return (False, "Category too long (max 50 characters)")

    return (True, "")


def validate_todo_id(todo_id_str: str) -> Tuple[bool, int, str]:
    """
    Validate and parse a todo ID.

    Args:
        todo_id_str: The ID string to validate

    Returns:
        Tuple of (is_valid, parsed_id, error_message)
        If valid: (True, id_value, "")
        If invalid: (False, 0, "Error description")
    """
    if not todo_id_str or not todo_id_str.strip():
        return (False, 0, "Please enter a todo ID")

    try:
        todo_id = int(todo_id_str)
        if todo_id <= 0:
            return (False, 0, "Todo ID must be a positive number")
        return (True, todo_id, "")
    except ValueError:
        return (False, 0, "Invalid input: please enter a valid number")


def validate_menu_choice(choice_str: str, min_choice: int, max_choice: int) -> Tuple[bool, int, str]:
    """
    Validate a menu choice.

    Args:
        choice_str: The choice string to validate
        min_choice: Minimum valid choice
        max_choice: Maximum valid choice

    Returns:
        Tuple of (is_valid, parsed_choice, error_message)
    """
    if not choice_str or not choice_str.strip():
        return (False, 0, f"Please enter a number between {min_choice} and {max_choice}")

    try:
        choice = int(choice_str)
        if choice < min_choice or choice > max_choice:
            return (False, 0, f"Invalid choice. Please enter {min_choice}-{max_choice}")
        return (True, choice, "")
    except ValueError:
        return (False, 0, f"Invalid input. Please enter a number between {min_choice} and {max_choice}")


def validate_confirmation(response: str) -> bool:
    """
    Validate a yes/no confirmation response.

    Args:
        response: The user's response

    Returns:
        True if confirmed (yes/y), False otherwise
    """
    return response.lower() in ["yes", "y"]