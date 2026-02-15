# Backend Development Guide - Phase II

## Overview

This is the FastAPI backend for the Phase II Todo application. It provides RESTful APIs for user authentication and task management with JWT-based security.

## Technology Stack

- **Python**: 3.13+
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification (Better Auth tokens)
- **Security**: python-jose, passlib

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Must match frontend secret (generate with `openssl rand -hex 32`)
- `CORS_ORIGINS`: Frontend URL (default: http://localhost:3000)

### 4. Run Development Server

```bash
uvicorn main:app --reload
```

Backend runs at: **http://localhost:8000**

API documentation: **http://localhost:8000/docs**

## Project Structure

```
backend/
├── main.py              # Application entry point
├── core/
│   ├── config.py        # Settings management
│   ├── security.py      # JWT utilities
│   └── db.py            # Database connection
├── models/
│   ├── user.py          # User SQLModel
│   └── task.py          # Task SQLModel
├── services/
│   ├── auth_service.py  # Auth business logic
│   └── task_service.py  # Task business logic
├── routes/
│   ├── auth.py          # Auth endpoints
│   └── tasks.py         # Task endpoints
├── middleware/
│   └── auth.py          # JWT validation
└── tests/               # Test files
```

## Development Guidelines

### 1. Code Organization

- **Models**: Define SQLModel classes for database tables
- **Services**: Implement business logic (NO database queries in routes)
- **Routes**: Define API endpoints (thin controllers)
- **Middleware**: Cross-cutting concerns (auth, logging)

### 2. Security Rules

**CRITICAL**:
- ALL task queries MUST filter by `user_id`
- JWT token MUST be validated on every request (except `/auth/*`)
- URL `user_id` MUST match JWT `sub` claim
- Return 401 for invalid/missing tokens
- Return 403 for user_id mismatch

### 3. Error Handling

```python
from fastapi import HTTPException, status

# Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)

# Forbidden (user_id mismatch)
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden: user_id mismatch"
)

# Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)
```

### 4. Database Queries

**Always filter by user_id**:

```python
# Correct
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# WRONG - allows cross-user access
tasks = session.exec(select(Task)).all()
```

## API Endpoints

### Authentication (No JWT required)

- `POST /auth/register` - Create new user
- `POST /auth/login` - Login and receive JWT

### Tasks (JWT required)

- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Common Tasks

### Add New Endpoint

1. Define route in `routes/`
2. Implement business logic in `services/`
3. Add JWT dependency if protected
4. Verify user_id matches JWT
5. Test endpoint

### Add New Model

1. Create SQLModel in `models/`
2. Import in `main.py` for table creation
3. Create service layer in `services/`
4. Add routes in `routes/`

### Debug Database Issues

```bash
# Check connection
python -c "from core.db import engine; print(engine.connect())"

# View SQL queries
uvicorn main:app --reload --log-level debug
```

## Phase II Constraints

**Must NOT**:
- ❌ Add AI features
- ❌ Add MCP tools
- ❌ Add background jobs
- ❌ Add event-driven patterns
- ❌ Add Docker/Kubernetes

**Must HAVE**:
- ✅ Stateless authentication (JWT only)
- ✅ User isolation (100% filtering)
- ✅ Clean API boundaries
- ✅ Service layer abstraction

## Troubleshooting

### Database Connection Fails

- Check `DATABASE_URL` in `.env`
- Verify Neon database is active
- Test with: `psql $DATABASE_URL`

### JWT Verification Fails

- Ensure `BETTER_AUTH_SECRET` matches frontend
- Check token format: `Bearer <token>`
- Verify token not expired

### CORS Errors

- Check `CORS_ORIGINS` in `.env`
- Ensure frontend URL included
- Verify middleware configured in `main.py`

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLModel Docs: https://sqlmodel.tiangolo.com/
- Neon Docs: https://neon.tech/docs
- Specification: `/specs/001-fullstack-web-app/spec.md`
- Plan: `/specs/001-fullstack-web-app/plan.md`
