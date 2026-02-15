"""User model for authentication.

This model is managed by Better Auth on the frontend.
The backend only reads user data for JWT validation and task ownership.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model representing authenticated users.

    Better Auth manages user creation and authentication on the frontend.
    The backend only needs to read user data for authorization.
    """

    __tablename__ = "users"

    id: str = Field(primary_key=True, description="User ID from Better Auth")
    email: str = Field(unique=True, index=True, description="User email address")
    password_hash: str = Field(description="Bcrypt hashed password")
    name: Optional[str] = Field(default=None, description="User display name")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": "user_123abc",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
