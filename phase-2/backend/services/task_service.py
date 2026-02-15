"""Task service for CRUD operations on todo items.

CRITICAL SECURITY: All queries MUST filter by user_id to enforce user isolation.
"""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select

from models.task import Task, TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a task is not found or not owned by user."""
    pass


def list_tasks(session: Session, user_id: str) -> List[Task]:
    """List all tasks for a specific user.

    SECURITY: Only returns tasks owned by the authenticated user.

    Args:
        session: Database session
        user_id: Authenticated user's ID

    Returns:
        List[Task]: User's tasks, ordered by created_at descending (newest first)
    """
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )

    tasks = session.exec(statement).all()
    return list(tasks)


def get_task(session: Session, user_id: str, task_id: int) -> Task:
    """Get a specific task by ID, verifying ownership.

    SECURITY: Verifies task belongs to authenticated user.

    Args:
        session: Database session
        user_id: Authenticated user's ID
        task_id: Task ID to retrieve

    Returns:
        Task: The requested task

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: Verify ownership
    )

    task = session.exec(statement).first()

    if not task:
        raise TaskNotFoundError(
            f"Task {task_id} not found or does not belong to user"
        )

    return task


def create_task(
    session: Session,
    user_id: str,
    task_data: TaskCreate
) -> Task:
    """Create a new task for a user.

    Args:
        session: Database session
        user_id: Authenticated user's ID (becomes task owner)
        task_data: Task creation data (title, description)

    Returns:
        Task: Newly created task
    """
    now = datetime.utcnow()

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=now,
        updated_at=now,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def update_task(
    session: Session,
    user_id: str,
    task_id: int,
    task_data: TaskUpdate
) -> Task:
    """Update an existing task.

    SECURITY: Verifies task belongs to authenticated user.

    Args:
        session: Database session
        user_id: Authenticated user's ID
        task_id: Task ID to update
        task_data: Task update data (title, description)

    Returns:
        Task: Updated task

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    # Get task (includes ownership verification)
    task = get_task(session, user_id, task_id)

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def toggle_task_completion(
    session: Session,
    user_id: str,
    task_id: int
) -> Task:
    """Toggle a task's completion status.

    SECURITY: Verifies task belongs to authenticated user.

    Args:
        session: Database session
        user_id: Authenticated user's ID
        task_id: Task ID to toggle

    Returns:
        Task: Updated task with toggled completion status

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    # Get task (includes ownership verification)
    task = get_task(session, user_id, task_id)

    # Toggle completion
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, user_id: str, task_id: int) -> bool:
    """Delete a task.

    SECURITY: Verifies task belongs to authenticated user.

    Args:
        session: Database session
        user_id: Authenticated user's ID
        task_id: Task ID to delete

    Returns:
        bool: True if deleted successfully

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    # Get task (includes ownership verification)
    task = get_task(session, user_id, task_id)

    # Delete task
    session.delete(task)
    session.commit()

    return True
