# Implementation Plan: Phase II Full-Stack Web Application

**Branch**: `001-fullstack-web-app` | **Date**: 2026-02-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fullstack-web-app/spec.md`

**Note**: This plan follows the `/sp.plan` command workflow and defines a 7-layer execution strategy for transforming the Phase I console app into a production-grade multi-user web application.

## Summary

Transform the Phase I console-based Todo application into a modern, multi-user full-stack web application with:
- **Frontend**: Next.js 16+ with App Router for responsive, authenticated UI
- **Backend**: FastAPI with Python 3.13+ for RESTful API services
- **Database**: Neon Serverless PostgreSQL for persistent, scalable storage
- **Authentication**: Better Auth + JWT for stateless, secure multi-user access
- **Architecture**: Clean separation with strict API boundaries for Phase III extensibility

**Execution Strategy**: 7 controlled layers (monorepo setup → backend foundation → auth integration → task domain → REST API → frontend foundation → frontend integration) ensuring each component is validated before proceeding.

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: TypeScript 5.x with Next.js 16+

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, python-jose (JWT), python-multipart, uvicorn
- Frontend: Next.js 16+ (App Router), Better Auth, React 19+, Tailwind CSS
- Database: Neon Serverless PostgreSQL (via psycopg2-binary or asyncpg)

**Storage**:
- Neon Serverless PostgreSQL (cloud-hosted)
- Connection via DATABASE_URL environment variable
- Indexes on tasks.user_id and tasks.completed

**Testing**:
- Backend: pytest, pytest-asyncio for async tests
- Frontend: Jest, React Testing Library
- Integration: Manual E2E validation for Phase II

**Target Platform**:
- Backend: ASGI server (uvicorn) on localhost:8000 (development)
- Frontend: Next.js dev server on localhost:3000 (development)
- Database: Neon cloud platform

**Project Type**: Web application (frontend + backend monorepo)

**Performance Goals**:
- User registration: < 1 minute
- Login/authentication: < 10 seconds
- Task creation: < 15 seconds
- Task list load: < 2 seconds
- Task operations (update/delete/complete): < 3 seconds
- API response time: < 200ms p95 for simple queries
- Concurrent users: 100+ without degradation

**Constraints**:
- Stateless authentication (no server-side sessions)
- Zero cross-user data leakage (100% user isolation)
- JWT validation on every API request
- All database queries filtered by authenticated user_id
- No business logic in frontend (API calls only)
- Task title: 1-200 characters (required)
- Task description: max 1000 characters (optional)

**Scale/Scope**:
- Multi-user support (no hard limit for Phase II)
- 5 core operations: Add, View, Update, Delete, Mark Complete
- 6 user stories (3 P1, 2 P2, 1 P3)
- 28 functional requirements
- 14 success criteria
- Monorepo structure with Spec-Kit Plus compliance

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Spec-Driven Development**: Feature specification exists at `specs/001-fullstack-web-app/spec.md` and is complete (validated via requirements checklist)
- ✅ **Phase Compliance**: Implementation adheres to Phase II constraints (Next.js, FastAPI, Neon PostgreSQL, Better Auth as specified)
- ✅ **Technology Stack**: All tech choices align with phase-specific requirements (no deviation from approved stack)
- ✅ **Repository Structure**: Code placement follows monorepo organization with phase-2/ directory structure
- ✅ **Clean Code Standards**: Plan adheres to simplicity principles (service layer abstraction, no business logic in frontend, clear API boundaries)

**No violations detected.** Proceeding to implementation phases.

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-web-app/
├── spec.md                      # Feature specification (completed)
├── plan.md                      # This file (/sp.plan output)
├── contracts/                   # API contracts and schemas
│   ├── api-endpoints.md         # REST API specification
│   ├── data-models.md           # Entity schemas (User, Task)
│   └── auth-flow.md             # JWT authentication flow
├── checklists/                  # Quality validation
│   └── requirements.md          # Spec quality checklist (completed)
└── tasks.md                     # Phase 2 output (/sp.tasks - NOT YET CREATED)
```

### Source Code (repository root)

```text
phase-2/
├── backend/
│   ├── CLAUDE.md                # Backend-specific instructions
│   ├── main.py                  # FastAPI application entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variable template
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── security.py          # JWT verification utilities
│   │   └── db.py                # Database connection & engine
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User SQLModel (Better Auth managed)
│   │   └── task.py              # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py      # Task business logic (CRUD operations)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py             # Task API endpoints
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py              # JWT validation middleware
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py         # Authentication tests
│       ├── test_task_service.py # Service layer tests
│       └── test_task_routes.py  # API endpoint tests
│
├── frontend/
│   ├── CLAUDE.md                # Frontend-specific instructions
│   ├── package.json             # Node dependencies
│   ├── tsconfig.json            # TypeScript configuration
│   ├── tailwind.config.ts       # Tailwind CSS configuration
│   ├── next.config.ts           # Next.js configuration
│   ├── .env.local.example       # Environment variable template
│   ├── app/
│   │   ├── layout.tsx           # Root layout with auth context
│   │   ├── page.tsx             # Landing/redirect page
│   │   ├── register/
│   │   │   └── page.tsx         # User registration page
│   │   ├── login/
│   │   │   └── page.tsx         # User login page
│   │   ├── dashboard/
│   │   │   └── page.tsx         # Task list dashboard (protected)
│   │   └── tasks/
│   │       ├── [id]/
│   │       │   └── edit/
│   │       │       └── page.tsx # Edit task page (protected)
│   │       └── new/
│   │           └── page.tsx     # Create task page (protected)
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx    # Login form component
│   │   │   └── RegisterForm.tsx # Registration form component
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx     # Task list display
│   │   │   ├── TaskItem.tsx     # Individual task card
│   │   │   ├── TaskForm.tsx     # Create/edit task form
│   │   │   └── DeleteConfirm.tsx# Delete confirmation modal
│   │   └── ui/
│   │       ├── Button.tsx       # Reusable button component
│   │       ├── Input.tsx        # Reusable input component
│   │       ├── LoadingSpinner.tsx # Loading state indicator
│   │       └── ErrorMessage.tsx # Error state display
│   ├── lib/
│   │   ├── auth.ts              # Better Auth configuration
│   │   ├── api-client.ts        # Centralized API client (fetch wrapper)
│   │   └── utils.ts             # Utility functions
│   ├── services/
│   │   ├── task-service.ts      # Task API calls (uses api-client)
│   │   └── auth-service.ts      # Auth API calls (uses Better Auth)
│   └── types/
│       ├── task.ts              # Task type definitions
│       └── user.ts              # User type definitions
│
└── README.md                    # Monorepo documentation
```

**Structure Decision**: Selected **Option 2: Web application** structure with separate `backend/` and `frontend/` directories under `phase-2/`. This structure:
- Enforces clean separation of concerns (UI vs API vs data)
- Enables independent development and testing of frontend/backend
- Supports future Phase III extensibility (AI agents can consume backend APIs)
- Aligns with Spec-Kit Plus monorepo organization
- Facilitates Better Auth integration (frontend SDK + backend verification)

## Complexity Tracking

**No violations requiring justification.**

All architectural decisions align with constitutional principles:
- Single frontend project (Next.js)
- Single backend project (FastAPI)
- Service layer pattern justified by need for user-scoped data filtering
- Middleware pattern justified by need for JWT validation on every request

## Phase 0: Research & Technical Validation

### Objective
Validate technical feasibility of Better Auth + JWT integration and Neon PostgreSQL connectivity before implementation.

### Research Questions

1. **Better Auth + JWT Integration**
   - How does Better Auth issue JWT tokens in Next.js 16+ App Router?
   - What claims/payload structure does Better Auth use in JWTs?
   - How can FastAPI verify Better Auth JWT signatures using shared secret?
   - What library should backend use for JWT verification (python-jose, PyJWT)?

2. **Neon PostgreSQL Connection**
   - What is the connection string format for Neon Serverless PostgreSQL?
   - Does SQLModel work with Neon (PostgreSQL compatibility)?
   - Are there connection pooling considerations for serverless DB?
   - What are Neon-specific performance best practices?

3. **Authentication Flow**
   - Should Better Auth be configured for frontend-only or with backend integration?
   - Where should JWT tokens be stored on client side (httpOnly cookies vs localStorage)?
   - How to handle token refresh/expiration in Better Auth?
   - What is the user_id claim name in Better Auth JWTs?

4. **CORS Configuration**
   - What CORS headers does FastAPI need for Next.js frontend?
   - Should credentials be allowed in CORS for JWT cookies?
   - What origins should be whitelisted (localhost:3000 for dev)?

### Research Outputs

**Document findings in**: `specs/001-fullstack-web-app/research.md`

**Required sections**:
- Better Auth JWT structure and verification approach
- Neon PostgreSQL connection pattern and SQLModel compatibility
- Authentication flow diagram (user registration → login → API call)
- CORS configuration requirements
- Recommended libraries and versions

### Validation Criteria

- [ ] Proof of concept: Better Auth issues JWT in Next.js
- [ ] Proof of concept: FastAPI verifies Better Auth JWT signature
- [ ] Proof of concept: SQLModel connects to Neon PostgreSQL
- [ ] Authentication flow documented with sequence diagram
- [ ] All research questions answered with code examples

## Phase 1: Detailed Design

### Objective
Define concrete data models, API contracts, and authentication mechanisms based on Phase 0 research.

### 1.1 Data Model Design

**Document in**: `specs/001-fullstack-web-app/contracts/data-models.md`

#### User Entity (Better Auth Managed)

```typescript
// Frontend type definition
interface User {
  id: string;              // UUID from Better Auth
  email: string;           // Unique, validated
  createdAt: Date;         // Account creation timestamp
}
```

```python
# Backend SQLModel (reference only - Better Auth manages table)
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)  # UUID from Better Auth
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Notes**:
- User table is managed by Better Auth
- Backend only reads user_id from JWT, doesn't create/modify users directly
- Email uniqueness enforced by Better Auth

#### Task Entity (Backend Managed)

```typescript
// Frontend type definition
interface Task {
  id: number;              // Auto-increment primary key
  userId: string;          // Foreign key to User.id (UUID)
  title: string;           // 1-200 characters, required
  description: string | null; // Max 1000 characters, optional
  completed: boolean;      // Default: false
  createdAt: Date;         // Auto-set on creation
  updatedAt: Date;         // Auto-update on modification
}
```

```python
# Backend SQLModel
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Indexes**:
- `user_id` (for filtering tasks by owner)
- `completed` (for filtering by status)
- Composite index consideration: `(user_id, completed)` if status filtering is common

**Constraints**:
- `user_id` NOT NULL (every task must have an owner)
- `title` NOT NULL and length 1-200
- `description` nullable, max length 1000
- `completed` NOT NULL, default FALSE

### 1.2 API Contract Design

**Document in**: `specs/001-fullstack-web-app/contracts/api-endpoints.md`

**Base URL**: `http://localhost:8000/api`

**Authentication**: All endpoints require `Authorization: Bearer <JWT>` header

#### 1. List User Tasks

```http
GET /api/{user_id}/tasks
Authorization: Bearer <JWT>
```

**Request**:
- Path parameter: `user_id` (string, UUID)
- Headers: `Authorization: Bearer <JWT>`

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Complete project",
      "description": "Finish Phase II implementation",
      "completed": false,
      "createdAt": "2026-02-12T10:00:00Z",
      "updatedAt": "2026-02-12T10:00:00Z"
    }
  ]
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: user_id in URL doesn't match JWT user_id

#### 2. Create Task

```http
POST /api/{user_id}/tasks
Authorization: Bearer <JWT>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Validation**:
- `title`: required, 1-200 characters
- `description`: optional, max 1000 characters

**Response** (201 Created):
```json
{
  "id": 2,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "New task title",
  "description": "Optional task description",
  "completed": false,
  "createdAt": "2026-02-12T10:05:00Z",
  "updatedAt": "2026-02-12T10:05:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors (title missing, too long, etc.)
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: user_id in URL doesn't match JWT user_id

#### 3. Get Single Task

```http
GET /api/{user_id}/tasks/{task_id}
Authorization: Bearer <JWT>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete project",
  "description": "Finish Phase II implementation",
  "completed": false,
  "createdAt": "2026-02-12T10:00:00Z",
  "updatedAt": "2026-02-12T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: user_id in URL doesn't match JWT user_id
- `404 Not Found`: Task doesn't exist or belongs to different user

#### 4. Update Task

```http
PUT /api/{user_id}/tasks/{task_id}
Authorization: Bearer <JWT>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated title",
  "description": "Updated description",
  "completed": false,
  "createdAt": "2026-02-12T10:00:00Z",
  "updatedAt": "2026-02-12T10:10:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: user_id mismatch or task belongs to different user
- `404 Not Found`: Task doesn't exist

#### 5. Delete Task

```http
DELETE /api/{user_id}/tasks/{task_id}
Authorization: Bearer <JWT>
```

**Response** (204 No Content): Empty body

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: user_id mismatch or task belongs to different user
- `404 Not Found`: Task doesn't exist

#### 6. Toggle Task Completion

```http
PATCH /api/{user_id}/tasks/{task_id}/complete
Authorization: Bearer <JWT>
```

**Request Body**: Empty (toggles current state)

**Response** (200 OK):
```json
{
  "id": 1,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete project",
  "description": "Finish Phase II implementation",
  "completed": true,
  "createdAt": "2026-02-12T10:00:00Z",
  "updatedAt": "2026-02-12T10:15:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: user_id mismatch or task belongs to different user
- `404 Not Found`: Task doesn't exist

### 1.3 Authentication Flow Design

**Document in**: `specs/001-fullstack-web-app/contracts/auth-flow.md`

#### JWT Token Structure (Better Auth)

```json
{
  "sub": "123e4567-e89b-12d3-a456-426614174000",  // user_id
  "email": "user@example.com",
  "iat": 1707739200,
  "exp": 1707825600
}
```

**Claims**:
- `sub`: User ID (UUID) - used for user_id extraction
- `email`: User email (for display/reference)
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp

#### Authentication Sequence

```
User                Frontend (Next.js)         Backend (FastAPI)           Database
 |                        |                            |                        |
 |-- Register/Login ----->|                            |                        |
 |                        |-- Better Auth ------------>|                        |
 |                        |<-- JWT Token ------------- |                        |
 |<-- Redirect to --------|                            |                        |
 |    Dashboard           |                            |                        |
 |                        |                            |                        |
 |-- View Tasks --------->|                            |                        |
 |                        |-- GET /api/{uid}/tasks --->|                        |
 |                        |   Authorization: Bearer    |                        |
 |                        |                            |-- Verify JWT ------    |
 |                        |                            |   Extract user_id      |
 |                        |                            |   Check uid == token   |
 |                        |                            |                        |
 |                        |                            |-- SELECT * FROM ------>|
 |                        |                            |   tasks WHERE user_id  |
 |                        |                            |<-- Task List ----------|
 |                        |<-- Task JSON ------------- |                        |
 |<-- Render Tasks -------|                            |                        |
```

#### Backend JWT Verification Steps

1. **Extract JWT from Authorization header**
   - Format: `Bearer <token>`
   - Reject if header missing or malformed

2. **Verify JWT signature**
   - Use BETTER_AUTH_SECRET (shared with frontend)
   - Algorithm: HS256 (HMAC-SHA256)
   - Reject if signature invalid

3. **Check token expiration**
   - Compare `exp` claim with current timestamp
   - Reject if expired (401 Unauthorized)

4. **Extract user_id from `sub` claim**
   - This is the authenticated user ID

5. **Validate URL user_id parameter**
   - Compare URL `{user_id}` with token `sub` claim
   - Reject if mismatch (403 Forbidden)

6. **Proceed with user-scoped operation**
   - Filter all queries by authenticated user_id
   - Never trust client-provided user_id without JWT verification

### 1.4 Quick Start Guide

**Document in**: `specs/001-fullstack-web-app/quickstart.md`

Create a developer quickstart guide covering:

1. **Prerequisites**
   - Python 3.13+ installed
   - Node.js 20+ and npm installed
   - Neon PostgreSQL account and database created
   - Git repository cloned

2. **Backend Setup**
   ```bash
   cd phase-2/backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with DATABASE_URL and BETTER_AUTH_SECRET
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd phase-2/frontend
   npm install
   cp .env.local.example .env.local
   # Edit .env.local with BETTER_AUTH_SECRET and API_URL
   npm run dev
   ```

4. **Database Initialization**
   - Run migrations (manual for Phase II)
   - Create tables (users, tasks)
   - Verify connection

5. **Testing Authentication**
   - Register a user at http://localhost:3000/register
   - Login at http://localhost:3000/login
   - Verify JWT token in browser DevTools
   - Test protected route access

6. **Testing Task Operations**
   - Create a task
   - View task list
   - Update task
   - Toggle completion
   - Delete task

## Phase 2: Implementation Layers

### Layer 0: Monorepo & Spec-Kit Initialization

**Objective**: Establish Spec-Kit compliant project structure

**Tasks**:
1. Create `phase-2/` directory structure
2. Create `.spec-kit/config.yaml` if not exists
3. Create organized `/specs/` structure:
   - `specs/overview.md` (project overview)
   - `specs/architecture.md` (system architecture)
   - `specs/features/task-crud.md` (CRUD operations spec)
   - `specs/features/authentication.md` (auth spec)
   - `specs/api/rest-endpoints.md` (API contracts)
   - `specs/database/schema.md` (database schema)
   - `specs/ui/pages.md` (page specifications)
   - `specs/ui/components.md` (component specifications)
4. Create `phase-2/CLAUDE.md` (root instructions)
5. Create `phase-2/backend/CLAUDE.md` (backend-specific instructions)
6. Create `phase-2/frontend/CLAUDE.md` (frontend-specific instructions)
7. Create `phase-2/README.md` (developer documentation)

**Validation**:
- [ ] All spec files created and readable
- [ ] Folder structure matches plan
- [ ] CLAUDE.md files contain phase-specific guidance
- [ ] No application code exists yet

### Layer 1: Backend Foundation

**Objective**: Prepare backend for secure, persistent operations

**Tasks**:
1. Create `phase-2/backend/` directory
2. Initialize Python 3.13+ virtual environment
3. Create `requirements.txt`:
   ```
   fastapi==0.110.0
   uvicorn[standard]==0.27.1
   sqlmodel==0.0.16
   psycopg2-binary==2.9.9
   python-jose[cryptography]==3.3.0
   python-multipart==0.0.9
   pydantic-settings==2.2.1
   pytest==8.0.2
   pytest-asyncio==0.23.5
   ```
4. Create `backend/main.py` (FastAPI app entry point)
5. Create `backend/core/config.py` (settings management)
6. Create `backend/core/db.py` (SQLModel engine & session)
7. Create `.env.example`:
   ```
   DATABASE_URL=postgresql://user:pass@host/db
   BETTER_AUTH_SECRET=your-secret-here
   ```
8. Configure SQLModel engine for Neon PostgreSQL
9. Test database connection

**Validation**:
- [ ] Backend boots with `uvicorn main:app --reload`
- [ ] Database connection works (test with simple query)
- [ ] Environment variables loaded correctly
- [ ] No routes implemented yet

### Layer 2: Authentication Integration

**Objective**: Enable stateless authentication using Better Auth + JWT

**Tasks**:

**Backend**:
1. Create `backend/core/security.py` (JWT verification utilities)
2. Implement JWT verification function:
   ```python
   def verify_jwt(token: str) -> dict:
       # Verify signature using BETTER_AUTH_SECRET
       # Check expiration
       # Return payload with user_id
   ```
3. Create `backend/middleware/auth.py` (authentication middleware)
4. Implement dependency for extracting authenticated user_id:
   ```python
   async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
       payload = verify_jwt(token)
       return payload["sub"]  # user_id
   ```
5. Add CORS middleware to FastAPI app (allow localhost:3000)

**Frontend**:
1. Install Better Auth: `npm install better-auth`
2. Create `frontend/lib/auth.ts` (Better Auth configuration)
3. Configure Better Auth with JWT plugin
4. Implement token storage strategy (httpOnly cookies recommended)
5. Create auth context provider for app-wide access

**Validation**:
- [ ] Frontend Better Auth issues JWT on login
- [ ] Backend rejects requests without JWT (401)
- [ ] Backend rejects requests with invalid JWT (401)
- [ ] Backend successfully extracts user_id from valid JWT
- [ ] CORS allows frontend requests

### Layer 3: Task Domain & Persistence

**Objective**: Implement persistent task storage with user isolation

**Tasks**:
1. Create `backend/models/task.py` (Task SQLModel)
2. Define Task model with fields:
   - id (int, primary key, auto-increment)
   - user_id (str, foreign key, indexed)
   - title (str, 1-200 chars, required)
   - description (str | None, max 1000 chars)
   - completed (bool, default False, indexed)
   - created_at (datetime, auto-set)
   - updated_at (datetime, auto-update)
3. Create database migration (manual SQL for Phase II):
   ```sql
   CREATE TABLE tasks (
     id SERIAL PRIMARY KEY,
     user_id VARCHAR(36) NOT NULL,
     title VARCHAR(200) NOT NULL,
     description VARCHAR(1000),
     completed BOOLEAN NOT NULL DEFAULT FALSE,
     created_at TIMESTAMP NOT NULL DEFAULT NOW(),
     updated_at TIMESTAMP NOT NULL DEFAULT NOW()
   );
   CREATE INDEX idx_tasks_user_id ON tasks(user_id);
   CREATE INDEX idx_tasks_completed ON tasks(completed);
   ```
4. Create `backend/services/task_service.py` (business logic layer)
5. Implement service functions:
   - `create_task(user_id, title, description) -> Task`
   - `list_tasks(user_id) -> List[Task]`
   - `get_task(user_id, task_id) -> Task | None`
   - `update_task(user_id, task_id, title, description) -> Task | None`
   - `delete_task(user_id, task_id) -> bool`
   - `toggle_completion(user_id, task_id) -> Task | None`
6. **CRITICAL**: All service functions MUST filter by user_id

**Validation**:
- [ ] Task table created in Neon database
- [ ] Indexes exist on user_id and completed
- [ ] Service layer creates tasks successfully
- [ ] Service layer filters tasks by user_id (test with multiple users)
- [ ] Cross-user access impossible (verify isolation)
- [ ] Tasks persist across application restart

### Layer 4: REST API Enforcement

**Objective**: Expose secure, consistent REST endpoints

**Tasks**:
1. Create `backend/routes/tasks.py` (API route definitions)
2. Implement endpoint: `GET /api/{user_id}/tasks`
   - Validate JWT
   - Verify URL user_id matches JWT user_id
   - Call `task_service.list_tasks(user_id)`
   - Return JSON response
3. Implement endpoint: `POST /api/{user_id}/tasks`
   - Validate JWT and user_id
   - Validate request body (title required, description optional)
   - Call `task_service.create_task()`
   - Return 201 Created
4. Implement endpoint: `GET /api/{user_id}/tasks/{task_id}`
   - Validate JWT and user_id
   - Call `task_service.get_task()`
   - Return 404 if not found or belongs to different user
5. Implement endpoint: `PUT /api/{user_id}/tasks/{task_id}`
   - Validate JWT, user_id, request body
   - Call `task_service.update_task()`
   - Return updated task or 404
6. Implement endpoint: `DELETE /api/{user_id}/tasks/{task_id}`
   - Validate JWT and user_id
   - Call `task_service.delete_task()`
   - Return 204 No Content
7. Implement endpoint: `PATCH /api/{user_id}/tasks/{task_id}/complete`
   - Validate JWT and user_id
   - Call `task_service.toggle_completion()`
   - Return updated task
8. Add consistent error handling (401, 403, 404, 400 responses)
9. Register routes in `main.py`

**Validation**:
- [ ] All 6 endpoints respond correctly
- [ ] Unauthorized requests blocked (401)
- [ ] user_id mismatch blocked (403)
- [ ] Non-existent tasks return 404
- [ ] Validation errors return 400
- [ ] Response formats match API contracts
- [ ] Postman/curl tests pass for all endpoints

### Layer 5: Frontend Foundation

**Objective**: Prepare UI layer for authenticated interaction

**Tasks**:
1. Create `phase-2/frontend/` directory
2. Initialize Next.js 16+ with TypeScript:
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --app
   ```
3. Configure `tsconfig.json` for strict mode
4. Configure `tailwind.config.ts` with project theme
5. Create directory structure:
   - `app/` (Next.js App Router pages)
   - `components/` (React components)
   - `lib/` (utilities)
   - `services/` (API clients)
   - `types/` (TypeScript types)
6. Create `lib/api-client.ts` (centralized fetch wrapper):
   ```typescript
   async function apiClient(endpoint: string, options?: RequestInit) {
     const token = getAuthToken(); // Get JWT from storage
     const response = await fetch(`${API_URL}${endpoint}`, {
       ...options,
       headers: {
         'Authorization': `Bearer ${token}`,
         'Content-Type': 'application/json',
         ...options?.headers,
       },
     });
     if (!response.ok) throw new Error(`API error: ${response.status}`);
     return response.json();
   }
   ```
7. Create `types/task.ts` and `types/user.ts` (TypeScript interfaces)
8. Create `.env.local.example`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-secret-here
   ```

**Validation**:
- [ ] Next.js app runs at localhost:3000
- [ ] TypeScript compiles without errors
- [ ] Tailwind CSS applies correctly
- [ ] API client abstraction centralizes all calls
- [ ] No page content implemented yet

### Layer 6: Frontend Authentication Flow

**Objective**: Implement secure user login & protected routes

**Tasks**:
1. Create `app/register/page.tsx` (registration page)
2. Create `components/auth/RegisterForm.tsx`:
   - Email and password inputs
   - Form validation (email format, password strength)
   - Call Better Auth registration
   - Redirect to login on success
3. Create `app/login/page.tsx` (login page)
4. Create `components/auth/LoginForm.tsx`:
   - Email and password inputs
   - Call Better Auth login
   - Store JWT token securely
   - Redirect to dashboard on success
5. Implement auth context provider:
   - Track authentication state
   - Provide user_id to components
   - Handle token refresh
6. Create protected route middleware:
   - Check for valid JWT
   - Redirect to login if unauthenticated
7. Update `app/layout.tsx` to wrap with auth provider

**Validation**:
- [ ] User can register successfully
- [ ] User can log in successfully
- [ ] JWT token stored securely
- [ ] Protected routes redirect to login when unauthenticated
- [ ] Authenticated users can access dashboard
- [ ] Token included in API requests

### Layer 7: Frontend Task Workflows

**Objective**: Implement full CRUD UI

**Tasks**:
1. Create `services/task-service.ts` (API calls using api-client):
   ```typescript
   async function getTasks(userId: string): Promise<Task[]>
   async function createTask(userId: string, data: CreateTaskData): Promise<Task>
   async function updateTask(userId: string, taskId: number, data: UpdateTaskData): Promise<Task>
   async function deleteTask(userId: string, taskId: number): Promise<void>
   async function toggleComplete(userId: string, taskId: number): Promise<Task>
   ```

2. Create `app/dashboard/page.tsx` (task list page - protected):
   - Fetch tasks on load
   - Display task list
   - Show empty state if no tasks
   - Loading and error states

3. Create `components/tasks/TaskList.tsx`:
   - Map tasks to TaskItem components
   - Handle empty state

4. Create `components/tasks/TaskItem.tsx`:
   - Display task title, description, completed status
   - Edit button (links to /tasks/[id]/edit)
   - Delete button (shows confirmation modal)
   - Complete toggle checkbox

5. Create `app/tasks/new/page.tsx` (create task page - protected):
   - Task creation form
   - Title input (required, 1-200 chars)
   - Description textarea (optional, max 1000 chars)
   - Submit button
   - Cancel button

6. Create `components/tasks/TaskForm.tsx` (reusable form):
   - Form fields with validation
   - Submit handler
   - Error display

7. Create `app/tasks/[id]/edit/page.tsx` (edit task page - protected):
   - Load existing task data
   - Reuse TaskForm component
   - Update on submit

8. Create `components/tasks/DeleteConfirm.tsx` (confirmation modal):
   - Show task title
   - Confirm/Cancel buttons
   - Call deleteTask on confirm

9. Create UI components:
   - `components/ui/Button.tsx` (reusable button)
   - `components/ui/Input.tsx` (reusable input)
   - `components/ui/LoadingSpinner.tsx` (loading indicator)
   - `components/ui/ErrorMessage.tsx` (error display)

10. Implement loading and error states for all operations

**Validation**:
- [ ] User can view all their tasks
- [ ] User can create new tasks
- [ ] User can edit existing tasks
- [ ] User can delete tasks (with confirmation)
- [ ] User can toggle task completion
- [ ] Loading states display during async operations
- [ ] Error states display on failures
- [ ] UI is responsive on mobile and desktop
- [ ] All operations persist to backend

### Layer 8: Integration & Hardening

**Objective**: Finalize Phase II for production readiness

**Tasks**:
1. **End-to-End Testing**:
   - Register a new user
   - Login
   - Create 5 tasks
   - Update 2 tasks
   - Mark 3 tasks complete
   - Delete 1 task
   - Logout and login again
   - Verify all tasks persist correctly
   - Register second user
   - Verify user A cannot see user B's tasks

2. **Security Validation**:
   - Test with invalid JWT (should return 401)
   - Test with user_id mismatch (should return 403)
   - Test XSS prevention (special characters in task title/description)
   - Test SQL injection prevention (malicious input in fields)
   - Verify all queries filtered by user_id

3. **Performance Testing**:
   - Create 100 tasks for a user
   - Measure task list load time (should be < 2 seconds)
   - Measure task creation time (should be < 15 seconds)
   - Test with 10 concurrent users (manual or simple script)

4. **Documentation Updates**:
   - Update README.md with setup instructions
   - Update quickstart.md with latest steps
   - Document environment variables
   - Document API endpoints (OpenAPI/Swagger if time permits)

5. **Code Quality**:
   - Remove console.log statements
   - Remove commented code
   - Format code consistently (black for Python, prettier for TypeScript)
   - Add minimal comments for complex logic

**Validation**:
- [ ] All user stories (P1, P2, P3) work end-to-end
- [ ] All 28 functional requirements met
- [ ] All 14 success criteria achieved
- [ ] Zero cross-user data leakage
- [ ] Performance targets met
- [ ] Documentation complete and accurate

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| JWT secret mismatch between frontend/backend | Auth fails completely | Medium | Use shared BETTER_AUTH_SECRET env var; document in README; validate during Layer 2 |
| Cross-user data access vulnerability | Critical security breach | Low | Service layer enforces user_id filtering on ALL queries; Layer 3 validation required |
| Tight coupling between frontend/backend | Difficult to extend for Phase III | Medium | Strict API contract adherence; no business logic in frontend; service layer abstraction |
| Neon PostgreSQL connection issues | App cannot start | Low | Test connection early (Layer 1); provide clear error messages; document troubleshooting |
| Better Auth version incompatibility | Auth breaks after update | Low | Pin exact versions in package.json; test auth thoroughly in Layer 6 |
| Token storage security vulnerability | Token theft risk | Medium | Use httpOnly cookies (not localStorage); document security best practices |
| Database migration complexity | Schema drift | Medium | Manual migrations for Phase II; document schema in contracts/; version control migration files |
| CORS misconfiguration | Frontend cannot call backend | Medium | Configure CORS in Layer 2; test early; whitelist specific origins |
| Performance degradation with many tasks | Slow UI response | Low | No pagination for Phase II (acceptable); plan for Phase III optimization |
| Spec drift during implementation | Implementation doesn't match requirements | Medium | Always reference specs/001-fullstack-web-app/; update plan.md if changes needed; create ADRs for major decisions |

## Architectural Decision Records (ADRs)

Based on this plan, the following decisions meet the significance threshold for ADR documentation:

### ADR Candidates

1. **Authentication Architecture: Better Auth + JWT**
   - **Decision**: Use Better Auth for frontend authentication with JWT tokens verified by backend
   - **Alternatives**: NextAuth, Auth0, Custom auth, Sessions
   - **Impact**: Long-term authentication strategy for all phases
   - **Rationale**: Stateless architecture required for Phase III AI agents; Better Auth provides JWT support; shared secret enables backend verification
   - **Recommendation**: Create ADR after Layer 2 completion

2. **Data Isolation Strategy: Service Layer User Filtering**
   - **Decision**: Enforce user-scoped data access via service layer filtering (not database row-level security)
   - **Alternatives**: PostgreSQL row-level security (RLS), Application-level permissions, Separate databases per user
   - **Impact**: Security architecture for multi-user data isolation
   - **Rationale**: Service layer filtering is simpler for Phase II; RLS adds complexity; maintains flexibility for Phase III
   - **Recommendation**: Create ADR after Layer 3 completion

3. **API Contract: RESTful with User ID in URL**
   - **Decision**: Use `/api/{user_id}/tasks` pattern with user_id in URL path
   - **Alternatives**: Extract user_id from JWT only (no URL param), Session-based routing, GraphQL
   - **Impact**: API design for all endpoints
   - **Rationale**: Explicit user_id in URL makes ownership clear; enables double-verification (URL vs JWT); RESTful pattern familiar to developers
   - **Recommendation**: Create ADR after Layer 4 completion

4. **Frontend Architecture: Next.js App Router with Client Components**
   - **Decision**: Use Next.js 16+ App Router with client-side state management for tasks
   - **Alternatives**: Pages Router, Server Components only, SPA frameworks (React/Vue)
   - **Impact**: Frontend architecture and rendering strategy
   - **Rationale**: App Router is Next.js future; client components needed for auth context; aligns with Phase II requirements
   - **Recommendation**: Create ADR after Layer 5 completion

**ADR Creation Prompt**:
After completing the relevant layer, run:
```
/sp.adr <decision-title>
```

Example: `/sp.adr Authentication Architecture Better Auth JWT`

## Next Steps

1. **Begin Phase 0 Research** (if needed):
   - Research Better Auth JWT structure and verification
   - Test Neon PostgreSQL connectivity with SQLModel
   - Document findings in `research.md`

2. **Complete Phase 1 Design**:
   - Create all contract documents (data-models.md, api-endpoints.md, auth-flow.md)
   - Create quickstart.md
   - Review with team/stakeholders

3. **Generate Tasks** with `/sp.tasks`:
   - Convert this plan into actionable, testable tasks
   - Each layer becomes a series of tasks with acceptance criteria
   - Tasks will be dependency-ordered

4. **Execute Implementation**:
   - Follow Layer 0 → Layer 8 sequence
   - Validate each layer before proceeding
   - Create ADRs as decisions are implemented
   - Update plan.md if deviations occur

5. **Create PHR**:
   - Document this planning session in `history/prompts/001-fullstack-web-app/`
   - Record key decisions and rationale

---

**Plan Status**: Ready for Phase 1 design completion and task generation
**Next Command**: `/sp.tasks` to convert this plan into actionable tasks
**Estimated Effort**: 7 implementation layers × 4-8 hours per layer = 28-56 hours total development time
