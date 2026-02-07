from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from ..models import Task
from ..schemas import TaskCreate, TaskUpdate


class TaskService:
    @staticmethod
    def create_task(session: Session, task_data: TaskCreate) -> Task:
        task = Task(**task_data.model_dump())
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_all_tasks(session: Session) -> list[Task]:
        statement = select(Task).order_by(Task.created_at.desc())
        return list(session.exec(statement).all())

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID) -> Optional[Task]:
        return session.get(Task, task_id)

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
        task = session.get(Task, task_id)
        if not task:
            return None
        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID) -> bool:
        task = session.get(Task, task_id)
        if not task:
            return False
        session.delete(task)
        session.commit()
        return True
