# Data Models: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Created**: 2026-02-12
**Status**: Design Phase

## Overview

This document defines the conceptual data models for the Phase II multi-user todo application. These models represent the business entities without implementation-specific details.

## Entity Definitions

### User Entity

**Description**: Represents an authenticated application user with a unique identity and email address.

**Attributes**:
- **id**: Unique identifier (UUID format)
- **email**: Email address (unique, validated for format)
- **createdAt**: Timestamp when account was created

**Business Rules**:
- Email must be unique across all users
- Email must follow valid email format (validated by Better Auth)
- User accounts are created during registration process
- User identity is managed by Better Auth authentication system

**Relationships**:
- One user has many tasks (one-to-many)

**Notes**:
- User table is managed by Better Auth
- Backend does not directly create or modify user records
- Backend only references user_id from JWT tokens

### Task Entity

**Description**: Represents a todo item owned by a specific user, with title, optional description, and completion status.

**Attributes**:
- **id**: Unique identifier (auto-incrementing integer)
- **userId**: Reference to owning user (UUID, required)
- **title**: Short description of the task (1-200 characters, required)
- **description**: Detailed description (max 1000 characters, optional)
- **completed**: Completion status flag (boolean, default: false)
- **createdAt**: Timestamp when task was created (auto-set)
- **updatedAt**: Timestamp when task was last modified (auto-update)

**Business Rules**:
- Every task must belong to exactly one user
- Title is mandatory and must be 1-200 characters
- Description is optional; if provided, max 1000 characters
- Tasks default to incomplete (completed = false)
- Created timestamp is set automatically and never changes
- Updated timestamp is refreshed on every modification
- Tasks are isolated per user (no sharing capability)

**Relationships**:
- Many tasks belong to one user (many-to-one)

**Validation Rules**:
- Title length: 1 ≤ length ≤ 200
- Description length: 0 ≤ length ≤ 1000 (if provided)
- User ID must reference a valid user
- Completed must be boolean (true/false)

**Query Optimization**:
- Index on userId for filtering tasks by owner
- Index on completed for filtering by status
- Potential composite index on (userId, completed) for combined filtering

## Type Definitions

### Frontend (TypeScript)

```typescript
/**
 * User entity (Better Auth managed)
 */
interface User {
  id: string;              // UUID from Better Auth
  email: string;           // Unique, validated email address
  createdAt: Date;         // Account creation timestamp
}

/**
 * Task entity (backend managed)
 */
interface Task {
  id: number;              // Auto-increment primary key
  userId: string;          // Foreign key to User.id (UUID)
  title: string;           // Task title (1-200 characters)
  description: string | null; // Optional description (max 1000 chars)
  completed: boolean;      // Completion status (default: false)
  createdAt: Date;         // Creation timestamp
  updatedAt: Date;         // Last update timestamp
}

/**
 * Request payload for creating a task
 */
interface CreateTaskRequest {
  title: string;           // Required, 1-200 characters
  description?: string;    // Optional, max 1000 characters
}

/**
 * Request payload for updating a task
 */
interface UpdateTaskRequest {
  title: string;           // Required, 1-200 characters
  description?: string | null; // Optional, max 1000 characters
}
```

### Backend (Python SQLModel)

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    """
    User entity (managed by Better Auth)
    Backend references this table but does not create/modify records directly
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # UUID from Better Auth
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    """
    Task entity (managed by backend)
    Represents a todo item owned by a user
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Request model for creating a task"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskUpdate(SQLModel):
    """Request model for updating a task"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
```

## Database Schema (SQL)

**Phase II Setup**: Tables are automatically created by SQLModel on application startup via `create_db_tables()` in `backend/core/db.py`. The SQL below is provided for reference and manual setup if needed (e.g., for Neon PostgreSQL console).

**Production Note**: For production deployments, use proper database migrations (Alembic) instead of auto-creation.

### Neon PostgreSQL Schema

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);


-- Tasks table (managed by backend)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Optional: Composite index for user-scoped status filtering
CREATE INDEX idx_tasks_user_status ON tasks(user_id, completed);
```

**Manual Setup Instructions for Neon**:

1. Log into Neon Console (https://console.neon.tech)
2. Select your project and database
3. Open SQL Editor
4. Run the schema SQL above
5. Verify tables created: `\dt` in psql or check Tables tab

**Alternative**: SQLModel will auto-create tables on first `uvicorn` startup if `create_db_tables()` is called.

## Data Constraints

### User Constraints
- Email uniqueness enforced by database constraint
- Email format validation handled by Better Auth (not database)
- User ID is UUID (36 characters)

### Task Constraints
- User ID cannot be null (every task has an owner)
- Title cannot be null or empty
- Title length: 1-200 characters (enforced by application + database)
- Description length: 0-1000 characters (enforced by application + database)
- Completed defaults to FALSE
- Created/Updated timestamps cannot be null

## Edge Cases

1. **Task with maximum length title (200 characters)**
   - System should accept and store correctly
   - UI should display without truncation or overflow

2. **Task with maximum length description (1000 characters)**
   - System should accept and store correctly
   - UI should display in scrollable or expandable area

3. **Task with empty description**
   - Stored as NULL in database
   - Displayed as empty or placeholder in UI

4. **Task created and immediately updated**
   - created_at and updated_at will differ by milliseconds
   - System should handle rapid updates correctly

5. **User deleted from Better Auth**
   - Tasks become orphaned (user_id references non-existent user)
   - Phase II: Manual cleanup required
   - Phase III: Consider cascade delete or soft delete

6. **Concurrent task updates by same user (different tabs)**
   - Last write wins (no conflict resolution for Phase II)
   - updated_at reflects most recent change

## Future Considerations (Phase III+)

- **Task Categories/Tags**: Additional entity for organizing tasks
- **Task Priority**: Enum field (low, medium, high, urgent)
- **Task Due Dates**: Timestamp field for deadlines
- **Task Sharing**: Many-to-many relationship (task ↔ users)
- **Task Attachments**: Separate entity with file references
- **Task Comments**: Separate entity for collaboration
- **Task History/Audit Log**: Track all changes with timestamps
- **Soft Delete**: Add is_deleted flag instead of hard deletes
- **User Profile**: Extend user entity with name, avatar, preferences
