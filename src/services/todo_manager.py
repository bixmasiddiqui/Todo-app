"""Todo Manager service for managing todos in memory."""

from typing import List, Optional
from src.models.todo import Todo


class TodoManager:
    """
    Manages todos in memory with CRUD operations.

    The TodoManager maintains an in-memory list of todos and provides
    methods for adding, retrieving, updating, and deleting todos.
    """

    def __init__(self):
        """Initialize the TodoManager with empty todo list."""
        self._todos: List[Todo] = []
        self._next_id: int = 1

    def add(
        self,
        title: str,
        category: Optional[str] = None,
        priority: str = "medium",
    ) -> Todo:
        """
        Add a new todo.

        Args:
            title: Todo title (required, non-empty)
            category: Optional category label
            priority: Priority level (high/medium/low, default medium)

        Returns:
            The created Todo object

        Raises:
            ValueError: If title is empty or priority is invalid
        """
        todo = Todo(
            id=self._next_id,
            title=title,
            category=category,
            priority=priority,
        )
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def get_all(self) -> List[Todo]:
        """
        Get all todos in creation order.

        Returns:
            List of all todos (oldest first)
        """
        return self._todos.copy()

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Find a todo by ID.

        Args:
            todo_id: The ID of the todo to find

        Returns:
            The Todo if found, None otherwise
        """
        for todo in self._todos:
            if todo.id == todo_id:
                return todo
        return None

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Optional[Todo]:
        """
        Update a todo's fields.

        Args:
            todo_id: The ID of the todo to update
            title: New title (if provided)
            category: New category (if provided)
            priority: New priority (if provided)

        Returns:
            The updated Todo if found, None otherwise

        Raises:
            ValueError: If validation fails for any field
        """
        todo = self.get_by_id(todo_id)
        if todo is None:
            return None

        # Create a new todo with updated fields to trigger validation
        updated_todo = Todo(
            id=todo.id,
            title=title if title is not None else todo.title,
            completed=todo.completed,
            category=category if category is not None else todo.category,
            priority=priority if priority is not None else todo.priority,
            created_at=todo.created_at,
        )

        # Replace the old todo with the updated one
        for i, t in enumerate(self._todos):
            if t.id == todo_id:
                self._todos[i] = updated_todo
                return updated_todo

        return None

    def delete(self, todo_id: int) -> bool:
        """
        Delete a todo by ID.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if deleted, False if not found
        """
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                self._todos.pop(i)
                return True
        return False

    def mark_complete(self, todo_id: int, completed: bool = True) -> Optional[Todo]:
        """
        Mark a todo as complete or incomplete.

        Args:
            todo_id: The ID of the todo to update
            completed: True to mark complete, False for incomplete

        Returns:
            The updated Todo if found, None otherwise
        """
        todo = self.get_by_id(todo_id)
        if todo is None:
            return None

        todo.completed = completed
        return todo

    def get_by_category(self, category: str) -> List[Todo]:
        """
        Get all todos in a specific category.

        Args:
            category: The category to filter by (case-insensitive)

        Returns:
            List of todos in the category
        """
        category_lower = category.lower()
        return [t for t in self._todos if t.category == category_lower]

    def get_by_priority(self, priority: str) -> List[Todo]:
        """
        Get all todos with a specific priority.

        Args:
            priority: The priority to filter by (case-insensitive)

        Returns:
            List of todos with the priority
        """
        priority_lower = priority.lower()
        return [t for t in self._todos if t.priority == priority_lower]

    def count(self) -> int:
        """
        Get total number of todos.

        Returns:
            Total todo count
        """
        return len(self._todos)

    def count_completed(self) -> int:
        """
        Get number of completed todos.

        Returns:
            Count of completed todos
        """
        return sum(1 for todo in self._todos if todo.completed)
