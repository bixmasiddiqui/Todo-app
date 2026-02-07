"""API routes for task operations."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..database import get_db
from ..schemas import TaskCreate, TaskResponse, TaskUpdate
from ..services.task_service import TaskService

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_db),
) -> TaskResponse:
    """Create a new task.

    Args:
        task_data: Task creation data
        session: Database session

    Returns:
        TaskResponse: Created task

    Raises:
        HTTPException: 422 if validation fails
    """
    task = TaskService.create_task(session, task_data)
    return TaskResponse.model_validate(task)


@router.get("", response_model=list[TaskResponse])
async def get_all_tasks(
    session: Session = Depends(get_db),
) -> list[TaskResponse]:
    """Get all tasks ordered by creation date (newest first).

    Args:
        session: Database session

    Returns:
        list[TaskResponse]: List of all tasks
    """
    tasks = TaskService.get_all_tasks(session)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    session: Session = Depends(get_db),
) -> TaskResponse:
    """Get a task by ID.

    Args:
        task_id: Task UUID
        session: Database session

    Returns:
        TaskResponse: Task details

    Raises:
        HTTPException: 404 if task not found
    """
    task = TaskService.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return TaskResponse.model_validate(task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_db),
) -> TaskResponse:
    """Update a task.

    Args:
        task_id: Task UUID
        task_data: Task update data
        session: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 422 if validation fails
    """
    task = TaskService.update_task(session, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    session: Session = Depends(get_db),
) -> None:
    """Delete a task.

    Args:
        task_id: Task UUID
        session: Database session

    Raises:
        HTTPException: 404 if task not found
    """
    deleted = TaskService.delete_task(session, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
