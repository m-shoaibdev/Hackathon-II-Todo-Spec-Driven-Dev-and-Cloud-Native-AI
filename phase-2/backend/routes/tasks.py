"""Task routes for CRUD operations on todo items.

These routes handle:
- GET /api/{user_id}/tasks - List user's tasks
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{task_id} - Get specific task
- PUT /api/{user_id}/tasks/{task_id} - Update task
- PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion
- DELETE /api/{user_id}/tasks/{task_id} - Delete task

SECURITY: All routes verify user_id matches JWT token.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session

from core.db import get_session
from core.security import validate_user_id_match
from middleware.auth import CurrentUserId
from models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from services.task_service import (
    list_tasks,
    get_task,
    create_task,
    update_task,
    toggle_task_completion,
    delete_task,
    TaskNotFoundError,
)


router = APIRouter(tags=["Tasks"])


# Helper function to verify user_id matches JWT
def verify_user_access(url_user_id: str, current_user_id: CurrentUserId) -> str:
    """Verify that URL user_id matches authenticated user_id.

    Args:
        url_user_id: User ID from URL path
        current_user_id: User ID from JWT token

    Returns:
        str: Verified user_id

    Raises:
        HTTPException 403: If user_ids don't match
    """
    validate_user_id_match(current_user_id, url_user_id)
    return url_user_id


# Routes

@router.get(
    "/api/{user_id}/tasks",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List user's tasks",
    description="Get all tasks for the authenticated user, ordered by creation date (newest first).",
)
async def get_tasks(
    user_id: str = Path(..., description="User ID"),
    current_user_id: CurrentUserId = ...,
    session: Session = Depends(get_session),
) -> List[Task]:
    """List all tasks for the authenticated user.

    Args:
        user_id: User ID from URL (must match JWT)
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        List[Task]: User's tasks

    Raises:
        HTTPException 401: If JWT is invalid
        HTTPException 403: If user_id doesn't match JWT
    """
    # Verify user_id matches JWT
    verify_user_access(user_id, current_user_id)

    # Get tasks
    tasks = list_tasks(session, user_id)
    return tasks


@router.get(
    "/api/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get specific task",
    description="Get details of a specific task by ID.",
)
async def get_task_by_id(
    user_id: str = Path(..., description="User ID"),
    task_id: int = Path(..., description="Task ID"),
    current_user_id: CurrentUserId = ...,
    session: Session = Depends(get_session),
) -> Task:
    """Get a specific task by ID.

    Args:
        user_id: User ID from URL (must match JWT)
        task_id: Task ID
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Task: The requested task

    Raises:
        HTTPException 401: If JWT is invalid
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If task not found or not owned by user
    """
    # Verify user_id matches JWT
    verify_user_access(user_id, current_user_id)

    # Get task
    try:
        task = get_task(session, user_id, task_id)
        return task
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/api/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task",
    description="Create a new task for the authenticated user.",
)
async def create_new_task(
    user_id: str = Path(..., description="User ID"),
    task_data: TaskCreate = ...,
    current_user_id: CurrentUserId = ...,
    session: Session = Depends(get_session),
) -> Task:
    """Create a new task.

    Args:
        user_id: User ID from URL (must match JWT)
        task_data: Task creation data
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Task: Newly created task

    Raises:
        HTTPException 401: If JWT is invalid
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 422: If validation fails
    """
    # Verify user_id matches JWT
    verify_user_access(user_id, current_user_id)

    # Create task
    task = create_task(session, user_id, task_data)
    return task


@router.put(
    "/api/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task",
    description="Update an existing task's title and/or description.",
)
async def update_existing_task(
    user_id: str = Path(..., description="User ID"),
    task_id: int = Path(..., description="Task ID"),
    task_data: TaskUpdate = ...,
    current_user_id: CurrentUserId = ...,
    session: Session = Depends(get_session),
) -> Task:
    """Update an existing task.

    Args:
        user_id: User ID from URL (must match JWT)
        task_id: Task ID
        task_data: Task update data
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Task: Updated task

    Raises:
        HTTPException 401: If JWT is invalid
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If task not found or not owned by user
        HTTPException 422: If validation fails
    """
    # Verify user_id matches JWT
    verify_user_access(user_id, current_user_id)

    # Update task
    try:
        task = update_task(session, user_id, task_id, task_data)
        return task
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.patch(
    "/api/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion",
    description="Toggle a task's completion status (completed ↔ incomplete).",
)
async def toggle_task_complete(
    user_id: str = Path(..., description="User ID"),
    task_id: int = Path(..., description="Task ID"),
    current_user_id: CurrentUserId = ...,
    session: Session = Depends(get_session),
) -> Task:
    """Toggle task completion status.

    Args:
        user_id: User ID from URL (must match JWT)
        task_id: Task ID
        current_user_id: User ID from JWT token
        session: Database session

    Returns:
        Task: Task with toggled completion status

    Raises:
        HTTPException 401: If JWT is invalid
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If task not found or not owned by user
    """
    # Verify user_id matches JWT
    verify_user_access(user_id, current_user_id)

    # Toggle completion
    try:
        task = toggle_task_completion(session, user_id, task_id)
        return task
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/api/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Permanently delete a task.",
)
async def delete_existing_task(
    user_id: str = Path(..., description="User ID"),
    task_id: int = Path(..., description="Task ID"),
    current_user_id: CurrentUserId = ...,
    session: Session = Depends(get_session),
) -> None:
    """Delete a task.

    Args:
        user_id: User ID from URL (must match JWT)
        task_id: Task ID
        current_user_id: User ID from JWT token
        session: Database session

    Raises:
        HTTPException 401: If JWT is invalid
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If task not found or not owned by user
    """
    # Verify user_id matches JWT
    verify_user_access(user_id, current_user_id)

    # Delete task
    try:
        delete_task(session, user_id, task_id)
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
