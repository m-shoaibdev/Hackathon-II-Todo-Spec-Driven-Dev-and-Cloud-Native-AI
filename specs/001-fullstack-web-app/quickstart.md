# Quick Start Guide: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Created**: 2026-02-12
**Status**: Development Guide

## Overview

This guide walks you through setting up and running the Phase II full-stack todo application locally. Follow these steps in order to get the application running on your development machine.

## Prerequisites

Ensure you have the following installed before starting:

### Required Software

- **Python 3.13+**: [Download Python](https://www.python.org/downloads/)
  - Verify: `python --version` (should show 3.13.x or higher)

- **Node.js 20+** and **npm**: [Download Node.js](https://nodejs.org/)
  - Verify: `node --version` (should show 20.x or higher)
  - Verify: `npm --version`

- **Git**: [Download Git](https://git-scm.com/downloads)
  - Verify: `git --version`

### Required Accounts

- **Neon PostgreSQL Account**: [Sign up at neon.tech](https://neon.tech/)
  - Create a new project
  - Copy the connection string (format: `postgresql://user:pass@host/database`)

- **GitHub Repository** (if using version control):
  - Clone the repository: `git clone <repo-url>`
  - Navigate to project: `cd Hackathon-II-Todo-Spec-Driven-Dev-and-Cloud-Native-AI`

## Project Structure

```
Hackathon-II-Todo-Spec-Driven-Dev-and-Cloud-Native-AI/
├── phase-2/
│   ├── backend/          # FastAPI backend
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── .env          # Create this (copy from .env.example)
│   │   ├── core/
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   │
│   └── frontend/         # Next.js frontend
│       ├── app/
│       ├── components/
│       ├── lib/
│       ├── package.json
│       └── .env.local    # Create this (copy from .env.local.example)
│
└── specs/                # Feature specifications
    └── 001-fullstack-web-app/
```

## Setup Instructions

### Step 1: Backend Setup

#### 1.1 Navigate to Backend Directory

```bash
cd phase-2/backend
```

#### 1.2 Create Python Virtual Environment

**On macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows**:
```cmd
python -m venv venv
venv\Scripts\activate
```

**Verify activation**: Your terminal prompt should now show `(venv)` prefix

#### 1.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages**:
- fastapi
- uvicorn
- sqlmodel
- psycopg2-binary
- python-jose
- python-multipart
- pydantic-settings
- pytest

#### 1.4 Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
```

**Edit `.env` file** with your actual values:

```bash
# Database connection string from Neon
DATABASE_URL=postgresql://user:password@your-neon-host.neon.tech/your-database

# Shared secret for JWT (MUST match frontend)
# Generate strong secret: openssl rand -hex 32
BETTER_AUTH_SECRET=your-very-strong-secret-here-minimum-32-characters

# CORS allowed origins (frontend URL)
CORS_ORIGINS=http://localhost:3000
```

**CRITICAL**: The `BETTER_AUTH_SECRET` must be:
- At least 32 characters long
- Randomly generated (don't use predictable values)
- Identical in both backend and frontend `.env` files

**Generate strong secret** (recommended):
```bash
# macOS/Linux
openssl rand -hex 32

# Python (any OS)
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 1.5 Initialize Database

Run the database migration to create tables:

```bash
# If you have a migration script (TBD in implementation)
python scripts/init_db.py

# Or manually run SQL (connect to Neon console)
```

**SQL to run manually** (if needed):

```sql
-- Users table (managed by Better Auth)
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
```

#### 1.6 Start Backend Server

```bash
uvicorn main:app --reload
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify backend is running**:
- Open browser: http://localhost:8000
- Should see: `{"message": "Todo API is running"}` (or similar)
- API docs: http://localhost:8000/docs (FastAPI auto-generated)

**Leave this terminal running** and open a new terminal for frontend setup.

---

### Step 2: Frontend Setup

#### 2.1 Navigate to Frontend Directory

**In a NEW terminal window**:

```bash
cd phase-2/frontend
```

#### 2.2 Install Dependencies

```bash
npm install
```

**Expected packages** (from package.json):
- next
- react
- react-dom
- better-auth
- typescript
- tailwindcss
- etc.

**Installation time**: ~2-5 minutes depending on internet speed

#### 2.3 Configure Environment Variables

```bash
# Copy example env file
cp .env.local.example .env.local

# Edit .env.local with your values
```

**Edit `.env.local` file**:

```bash
# Better Auth secret (MUST match backend .env)
BETTER_AUTH_SECRET=your-very-strong-secret-here-minimum-32-characters

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth URL (frontend)
NEXT_PUBLIC_AUTH_URL=http://localhost:3000
```

**CRITICAL**: The `BETTER_AUTH_SECRET` must be **exactly the same** as backend `.env` file.

#### 2.4 Start Frontend Development Server

```bash
npm run dev
```

**Expected output**:
```
> frontend@0.1.0 dev
> next dev

  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.5s
```

**Verify frontend is running**:
- Open browser: http://localhost:3000
- Should see the application landing page

---

### Step 3: Verify Setup

#### 3.1 Check Both Services Running

- Backend: http://localhost:8000/docs (FastAPI Swagger UI)
- Frontend: http://localhost:3000 (Next.js app)

#### 3.2 Test Database Connection

**Backend terminal** should show successful database connection on startup.

**If connection fails**:
- Verify `DATABASE_URL` in backend `.env` is correct
- Check Neon PostgreSQL dashboard for database status
- Ensure IP is whitelisted in Neon (if required)

---

## First Run: Testing the Application

### Test 1: User Registration

1. **Navigate to registration page**: http://localhost:3000/register
2. **Fill form**:
   - Email: `test@example.com`
   - Password: `SecurePass123!`
3. **Click "Register"**
4. **Expected**: Redirect to login page with success message

### Test 2: User Login

1. **Navigate to login page**: http://localhost:3000/login (or already there from registration)
2. **Fill form**:
   - Email: `test@example.com`
   - Password: `SecurePass123!`
3. **Click "Login"**
4. **Expected**: Redirect to dashboard at http://localhost:3000/dashboard

### Test 3: Create a Task

1. **On dashboard**, click "Add Task" or "New Task" button
2. **Fill form**:
   - Title: `Complete Phase II implementation`
   - Description: `Finish all 7 implementation layers`
3. **Click "Save" or "Create"**
4. **Expected**: Task appears in task list

### Test 4: View Task List

1. **On dashboard**, verify task list displays
2. **Expected**: See the task you just created
3. **Verify**: Task shows title, description, and incomplete status

### Test 5: Mark Task Complete

1. **On dashboard**, click checkbox or "Complete" button for task
2. **Expected**: Task status changes to completed (visual indicator)
3. **Refresh page**: Task still shows as completed (persistence verified)

### Test 6: Edit Task

1. **Click "Edit" button** on task
2. **Modify**:
   - Title: `Complete Phase II implementation (IN PROGRESS)`
   - Description: `Currently on Layer 3`
3. **Save changes**
4. **Expected**: Updated task appears in list

### Test 7: Delete Task

1. **Click "Delete" button** on task
2. **Confirm deletion** in modal/dialog
3. **Expected**: Task removed from list
4. **Refresh page**: Task does not reappear (permanent deletion)

### Test 8: User Isolation

1. **Open incognito/private browser window**
2. **Register second user**: `user2@example.com`
3. **Login as user2**
4. **Create task** as user2
5. **Expected**: User2 sees only their tasks, not User1's tasks
6. **Verify isolation**: Switch back to User1's browser → User1 still sees only their tasks

---

## Troubleshooting

### Backend Issues

#### "Module not found" error
**Solution**: Activate virtual environment and reinstall dependencies
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### "Could not connect to database"
**Solution**: Verify DATABASE_URL in `.env`
- Check Neon dashboard for correct connection string
- Ensure database exists and is running
- Test connection with psql or DBeaver

#### "Port 8000 already in use"
**Solution**: Kill existing process or use different port
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn main:app --reload --port 8001
```

### Frontend Issues

#### "npm install" fails
**Solution**: Clear cache and retry
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### "NEXT_PUBLIC_API_URL is not defined"
**Solution**: Restart dev server after changing `.env.local`
- Stop server (Ctrl+C)
- Verify `.env.local` exists and contains `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Restart: `npm run dev`

#### "Failed to fetch" or CORS errors
**Solution**: Verify backend is running and CORS configured
- Check backend is running at http://localhost:8000
- Verify `CORS_ORIGINS=http://localhost:3000` in backend `.env`
- Check browser console for specific CORS error

### Authentication Issues

#### "Invalid token" or "401 Unauthorized"
**Solution**: Verify BETTER_AUTH_SECRET matches in both .env files
- Compare `BETTER_AUTH_SECRET` in `backend/.env` and `frontend/.env.local`
- Must be exactly identical (case-sensitive)
- Logout and login again after changing secret

#### "403 Forbidden" when accessing tasks
**Solution**: user_id mismatch
- This is a security feature (working correctly)
- Don't manually modify URLs with other user IDs
- Only access your own user_id routes

---

## Development Workflow

### Daily Development

1. **Start backend**:
   ```bash
   cd phase-2/backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   uvicorn main:app --reload
   ```

2. **Start frontend** (new terminal):
   ```bash
   cd phase-2/frontend
   npm run dev
   ```

3. **Make changes** to code (auto-reloads in both backend and frontend)

4. **Test changes** in browser at http://localhost:3000

### Running Tests

**Backend tests**:
```bash
cd phase-2/backend
source venv/bin/activate
pytest
```

**Frontend tests**:
```bash
cd phase-2/frontend
npm test
```

### Viewing Logs

**Backend logs**: Check terminal where `uvicorn` is running

**Frontend logs**:
- Terminal: Build/compile logs
- Browser DevTools → Console: Runtime logs

**Database logs**: Check Neon dashboard

---

## Next Steps

Once you've verified the application works:

1. **Explore the codebase**:
   - Backend: `phase-2/backend/routes/tasks.py` (API endpoints)
   - Frontend: `phase-2/frontend/app/dashboard/page.tsx` (main UI)

2. **Read the specifications**:
   - `specs/001-fullstack-web-app/spec.md` (requirements)
   - `specs/001-fullstack-web-app/plan.md` (architecture)
   - `specs/001-fullstack-web-app/contracts/` (API contracts)

3. **Review the implementation plan**:
   - 7 implementation layers defined in `plan.md`
   - Follow Layer 0 → Layer 8 sequence

4. **Start implementing** (if not already done):
   - Follow the plan's layer-by-layer approach
   - Validate each layer before proceeding

5. **Create tasks** with `/sp.tasks`:
   - Convert plan into actionable tasks
   - Track progress through implementation

---

## Getting Help

- **Specification**: `specs/001-fullstack-web-app/spec.md`
- **Architecture Plan**: `specs/001-fullstack-web-app/plan.md`
- **API Contracts**: `specs/001-fullstack-web-app/contracts/api-endpoints.md`
- **Data Models**: `specs/001-fullstack-web-app/contracts/data-models.md`
- **Auth Flow**: `specs/001-fullstack-web-app/contracts/auth-flow.md`

**Common commands**:
- Backend server: `uvicorn main:app --reload`
- Frontend server: `npm run dev`
- Run tests: `pytest` (backend) or `npm test` (frontend)
- Format code: `black .` (backend) or `npm run format` (frontend)

---

**Setup complete!** You should now have a fully functional development environment for the Phase II full-stack todo application.
