"""Business logic for task operations."""
from datetime import datetime
from uuid import UUID

from sqlmodel import Session, select

from ..models import Task
from ..schemas import TaskCreate, TaskUpdate


class TaskService:
    """Service layer for task operations."""

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate) -> Task:
        """Create a new task.

        Args:
            session: Database session
            task_data: Task creation data

        Returns:
            Task: Created task instance
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_all_tasks(session: Session) -> list[Task]:
        """Get all tasks ordered by creation date (newest first).

        Args:
            session: Database session

        Returns:
            list[Task]: List of all tasks
        """
        statement = select(Task).order_by(Task.created_at.desc())
        tasks = session.exec(statement).all()
        return list(tasks)

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID) -> Task | None:
        """Get a task by ID.

        Args:
            session: Database session
            task_id: Task UUID

        Returns:
            Task | None: Task instance if found, None otherwise
        """
        return session.get(Task, task_id)

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_data: TaskUpdate) -> Task | None:
        """Update a task.

        Args:
            session: Database session
            task_id: Task UUID
            task_data: Task update data

        Returns:
            Task | None: Updated task instance if found, None otherwise
        """
        task = session.get(Task, task_id)
        if not task:
            return None

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID) -> bool:
        """Delete a task.

        Args:
            session: Database session
            task_id: Task UUID

        Returns:
            bool: True if task was deleted, False if not found
        """
        task = session.get(Task, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True
