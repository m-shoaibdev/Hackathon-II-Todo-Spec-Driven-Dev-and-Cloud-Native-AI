"""Task model for todo items with user isolation."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task model representing a todo item.

    SECURITY: All queries MUST filter by user_id to enforce user isolation.
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True, description="Auto-increment task ID")
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner user ID - CRITICAL for user isolation"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )
    completed: bool = Field(
        default=False,
        description="Completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user_123abc",
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API docs",
                "completed": False,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class TaskCreate(SQLModel):
    """Schema for creating a new task.

    XSS Prevention: Pydantic validates and sanitizes input.
    React automatically escapes output when rendering.
    No HTML tags are processed - all user input treated as plain text.
    """

    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Updated task description (max 1000 characters)"
    )


class TaskResponse(SQLModel):
    """Schema for task responses to frontend."""

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
