# Phase II: Full-Stack Web Application

**Project**: Evolution of Todo
**Phase**: Phase II - Multi-user web application with authentication

## Overview

This directory contains the Phase II implementation of the Todo application, transforming the Phase I console app into a modern, multi-user full-stack web application.

## Architecture

```
phase-2/
├── backend/         # FastAPI backend (Python 3.13+)
├── frontend/        # Next.js frontend (TypeScript, App Router)
└── README.md        # This file
```

### Technology Stack

**Backend**:
- Python 3.13+
- FastAPI (REST API framework)
- SQLModel (ORM for PostgreSQL)
- Neon Serverless PostgreSQL (database)
- python-jose (JWT token verification)
- Better Auth JWT validation

**Frontend**:
- Next.js 16+ (React framework with App Router)
- TypeScript 5.x
- Better Auth (authentication with JWT)
- Tailwind CSS (styling)
- React 19+

## Key Features

- **Multi-user support**: Each user has isolated task lists
- **JWT Authentication**: Stateless authentication using Better Auth
- **RESTful API**: Clean API boundaries for Phase III extensibility
- **User Isolation**: 100% data filtering by authenticated user_id
- **5 Core Operations**: Add, View, Update, Delete, Mark Complete

## Getting Started

### Prerequisites

- Python 3.13 or higher
- Node.js 20 or higher
- Neon PostgreSQL account (database)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET
uvicorn main:app --reload
```

Backend runs at: **http://localhost:8000**

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with BETTER_AUTH_SECRET (must match backend)
npm run dev
```

Frontend runs at: **http://localhost:3000**

## Directory Structure

### Backend (`backend/`)

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── core/
│   ├── config.py        # Configuration management
│   ├── security.py      # JWT verification utilities
│   └── db.py            # Database connection & session
├── models/
│   ├── user.py          # User SQLModel (Better Auth managed)
│   └── task.py          # Task SQLModel
├── services/
│   ├── auth_service.py  # Authentication logic
│   └── task_service.py  # Task business logic (CRUD)
├── routes/
│   ├── auth.py          # Auth endpoints (register, login)
│   └── tasks.py         # Task endpoints (6 REST endpoints)
├── middleware/
│   └── auth.py          # JWT validation middleware
└── tests/               # Test files
```

### Frontend (`frontend/`)

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx       # Root layout with auth provider
│   ├── page.tsx         # Landing page
│   ├── register/        # Registration page
│   ├── login/           # Login page
│   ├── dashboard/       # Task list (protected)
│   └── tasks/           # Task create/edit pages
│       ├── new/         # Create new task
│       └── [id]/edit/   # Edit existing task
├── components/
│   ├── auth/            # Auth components (LoginForm, RegisterForm)
│   ├── tasks/           # Task components (TaskList, TaskItem, TaskForm, DeleteConfirm)
│   └── ui/              # Reusable UI components (Button, Input, LoadingSpinner, ErrorMessage)
├── contexts/
│   └── AuthContext.tsx  # Global auth state provider
├── lib/
│   ├── auth.ts          # Better Auth configuration
│   └── api-client.ts    # API client wrapper with error handling
├── services/
│   └── task-service.ts  # Task API calls (CRUD operations)
└── types/
    ├── user.ts          # User TypeScript types
    └── task.ts          # Task TypeScript types with validation
```

## API Endpoints

**Base URL**: `http://localhost:8000/api`

**Authentication**:
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token

**Tasks** (all require JWT):
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Security

- **JWT Validation**: All task endpoints require valid JWT token
- **User ID Verification**: URL user_id must match JWT user_id (403 Forbidden if mismatch)
- **Data Isolation**: All queries filtered by authenticated user_id
- **No Cross-User Access**: Users can only access their own tasks
- **Stateless**: No server-side sessions (all state in JWT)

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Environment Variables

Both backend and frontend require `BETTER_AUTH_SECRET` to be **identical**.

**Backend (.env)**:
```
DATABASE_URL=postgresql://user:pass@host/database
BETTER_AUTH_SECRET=your-secret-here-min-32-chars
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local)**:
```
BETTER_AUTH_SECRET=your-secret-here-min-32-chars
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:3000
```

## Testing

Manual end-to-end validation scenarios are defined in `/specs/001-fullstack-web-app/quickstart.md`.

**Key test scenarios**:
1. User registration
2. User login
3. Create task
4. View task list
5. Update task
6. Mark task complete
7. Delete task
8. User isolation (verify no cross-user access)

## Phase II Constraints

This implementation adheres to Phase II constraints:
- ❌ No AI agents
- ❌ No MCP tools
- ❌ No Kubernetes
- ❌ No Docker deployment
- ❌ No event-driven architecture
- ❌ No recurring tasks or reminders

Phase III will add:
- AI agent integration
- Advanced features
- Cloud deployment

## Documentation

- **Specification**: `/specs/001-fullstack-web-app/spec.md`
- **Architecture Plan**: `/specs/001-fullstack-web-app/plan.md`
- **Implementation Tasks**: `/specs/001-fullstack-web-app/tasks.md`
- **API Contracts**: `/specs/001-fullstack-web-app/contracts/`
- **Quick Start Guide**: `/specs/001-fullstack-web-app/quickstart.md`

## License

[Your License Here]

## Contributing

This project follows Spec-Kit Plus workflow. All changes must:
1. Have a corresponding specification
2. Follow the implementation plan
3. Complete all task checkpoints
4. Maintain Phase II constraints
