"""Main CLI application for Todo Manager."""

from src.services.todo_manager import TodoManager
from src.cli.menu import display_main_menu, get_menu_choice, clear_screen
from src.cli.commands import handle_add_todo, handle_list_todos, handle_exit
from src.lib.validators import validate_menu_choice
from src.lib.formatters import format_welcome_banner, format_error


def show_welcome() -> None:
    """Display welcome banner and wait for user to continue."""
    print(format_welcome_banner())
    input()  # Wait for ENTER
    clear_screen()


def run() -> None:
    """
    Run the main CLI application loop.

    Creates a TodoManager instance and processes user commands
    until the user chooses to exit.
    """
    # Show welcome banner
    show_welcome()

    # Create the todo manager (in-memory storage)
    manager = TodoManager()

    # Main application loop
    while True:
        clear_screen()
        display_main_menu()

        # Get user choice
        choice_str = get_menu_choice()

        # Validate choice
        is_valid, choice, error = validate_menu_choice(choice_str, 1, 3)

        if not is_valid:
            print("\n" + format_error(error))
            from src.cli.menu import pause_for_user
            pause_for_user()
            continue

        # Handle the command
        clear_screen()

        if choice == 1:
            # Add new todo
            handle_add_todo(manager)

        elif choice == 2:
            # List all todos
            handle_list_todos(manager)

        elif choice == 3:
            # Exit
            handle_exit()
            break

        # Unknown choice (should not happen due to validation)
        else:
            print("\n" + format_error("Invalid choice"))
            from src.cli.menu import pause_for_user
            pause_for_user()
