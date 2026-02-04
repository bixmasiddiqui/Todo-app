"""CLI menu display and input handling."""

from src.lib.formatters import format_header


def display_main_menu() -> None:
    """
    Display the main menu options.

    Shows all available commands for User Story 1 (Add and View todos).
    """
    print("\n" + format_header("TODO MANAGER"))
    print("\nAvailable Commands:")
    print("  1. Add new todo")
    print("  2. List all todos")
    print("  3. Exit")
    print("\n" + "=" * 64)


def get_menu_choice() -> str:
    """
    Get user's menu choice from standard input.

    Returns:
        User's input as string (to be validated by caller)
    """
    choice = input("\nEnter your choice (1-3): ").strip()
    return choice


def get_todo_input() -> dict:
    """
    Get todo details from user input.

    Prompts for title, category (optional), and priority (optional).

    Returns:
        Dictionary with keys: 'title', 'category', 'priority'
    """
    print("\n" + format_header("ADD NEW TODO", width=64))

    title = input("\nTodo title (required): ").strip()

    category = input("Category (optional, press Enter to skip): ").strip()
    if not category:
        category = None

    priority = input("Priority [high/medium/low] (default: medium): ").strip()
    if not priority:
        priority = "medium"

    return {
        "title": title,
        "category": category,
        "priority": priority,
    }


def pause_for_user() -> None:
    """
    Pause and wait for user to press Enter.

    Used after displaying messages to keep them visible.
    """
    input("\nPress ENTER to continue...")


def clear_screen() -> None:
    """
    Clear the console screen.

    Uses platform-specific commands (cls for Windows, clear for Unix).
    Note: For Phase I, we keep it simple and just print newlines.
    """
    # Simple approach: print multiple newlines to "clear" screen
    # In Phase II+, could use os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 2)
