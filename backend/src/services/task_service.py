"""Business logic for task operations."""
import logging
from datetime import datetime
from uuid import UUID

from sqlmodel import Session, select

from ..config import settings
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate

logger = logging.getLogger(__name__)

# Lazy-init Kafka producer (only when enabled)
_event_producer = None


def _get_event_producer():
    global _event_producer
    if _event_producer is None and settings.kafka_enabled:
        try:
            from ..events.kafka_producer import TaskEventProducer
            _event_producer = TaskEventProducer(settings.kafka_bootstrap_servers)
        except Exception as e:
            logger.warning(f"Kafka producer unavailable: {e}")
    return _event_producer


class TaskService:
    """Service layer for task operations."""

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: UUID) -> Task:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id,
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        producer = _get_event_producer()
        if producer:
            producer.task_created(task.id, task.title)

        return task

    @staticmethod
    def get_all_tasks(session: Session, user_id: UUID) -> list[Task]:
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        tasks = session.exec(statement).all()
        return list(tasks)

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Task | None:
        task = session.get(Task, task_id)
        if task and task.user_id != user_id:
            return None
        return task

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_data: TaskUpdate, user_id: UUID) -> Task | None:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
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

        producer = _get_event_producer()
        if producer:
            changes = task_data.model_dump(exclude_unset=True)
            producer.task_updated(task.id, changes)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return False

        session.delete(task)
        session.commit()

        producer = _get_event_producer()
        if producer:
            producer.task_deleted(task_id)

        return True
