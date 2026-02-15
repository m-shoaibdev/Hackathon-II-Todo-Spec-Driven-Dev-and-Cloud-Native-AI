---
description: "Task list for Phase II Full-Stack Web Application implementation"
---

# Tasks: Phase II Full-Stack Web Application

**Input**: Design documents from `/specs/001-fullstack-web-app/`
**Prerequisites**: plan.md, spec.md, contracts/ (api-endpoints.md, data-models.md, auth-flow.md), quickstart.md

**Constitutional Compliance**: All tasks must adhere to Phase II constraints and technology stack defined in the project constitution.

**Tests**: Tests are NOT included - manual E2E validation per quickstart.md is specified for Phase II.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `phase-2/backend/`
- **Frontend**: `phase-2/frontend/`
- Monorepo structure as defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure setup

- [ ] T001 Create phase-2/ directory with README.md documenting monorepo structure
- [ ] T002 Create phase-2/backend/ directory structure (core/, models/, routes/, services/, middleware/, tests/)
- [ ] T003 Create phase-2/frontend/ directory structure (app/, components/, lib/, services/, types/)
- [ ] T004 Create phase-2/backend/requirements.txt with FastAPI, SQLModel, python-jose, uvicorn, pydantic-settings, psycopg2-binary
- [ ] T005 Create phase-2/backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS placeholders
- [ ] T006 Create phase-2/backend/main.py as FastAPI application entry point
- [ ] T007 [P] Create phase-2/backend/core/config.py for environment-based configuration management
- [ ] T008 [P] Create phase-2/frontend/.env.local.example with BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL, NEXT_PUBLIC_AUTH_URL placeholders
- [ ] T009 Initialize Next.js 16+ with TypeScript in phase-2/frontend/ using App Router
- [ ] T010 Configure Tailwind CSS in phase-2/frontend/tailwind.config.ts
- [ ] T011 [P] Create phase-2/backend/CLAUDE.md with backend-specific development instructions
- [ ] T012 [P] Create phase-2/frontend/CLAUDE.md with frontend-specific development instructions

**Checkpoint**: Project structure initialized, ready for foundational infrastructure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 Create phase-2/backend/core/db.py with SQLModel engine and session management for Neon PostgreSQL
- [ ] T014 Configure CORS middleware in phase-2/backend/main.py allowing http://localhost:3000
- [ ] T015 Create phase-2/backend/models/user.py with User SQLModel (id, email, created_at) managed by Better Auth
- [ ] T016 Create phase-2/backend/models/task.py with Task SQLModel (id, user_id, title, description, completed, created_at, updated_at)
- [ ] T017 Create database initialization script or manual SQL in specs/001-fullstack-web-app/contracts/data-models.md for Neon
- [ ] T018 Create phase-2/backend/core/security.py with JWT verification utility using python-jose and BETTER_AUTH_SECRET
- [ ] T019 Create phase-2/backend/middleware/auth.py with JWT validation dependency (get_current_user_id)
- [ ] T020 Create phase-2/frontend/lib/auth.ts with Better Auth configuration and JWT plugin setup
- [ ] T021 Create phase-2/frontend/lib/api-client.ts as centralized fetch wrapper with JWT token attachment
- [ ] T022 Create phase-2/frontend/types/user.ts with User interface (id, email, createdAt)
- [ ] T023 Create phase-2/frontend/types/task.ts with Task interface (id, userId, title, description, completed, createdAt, updatedAt)

**Checkpoint**: Foundation ready - authentication, database, and API client infrastructure complete. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and log in with JWT token issuance for secure access to protected routes

**Independent Test**: Register a new user, login, verify JWT token issuance and storage, access protected routes successfully

### Implementation for User Story 1

**Backend Authentication Services:**

- [ ] T024 [P] [US1] Create phase-2/backend/services/auth_service.py with password hashing utility (bcrypt/passlib)
- [ ] T025 [P] [US1] Implement user registration service in phase-2/backend/services/auth_service.py (hash password, create user, prevent duplicate emails)
- [ ] T026 [P] [US1] Implement user login service in phase-2/backend/services/auth_service.py (verify credentials, generate JWT token)
- [ ] T027 [US1] Create phase-2/backend/routes/auth.py with POST /auth/register endpoint (calls registration service)
- [ ] T028 [US1] Implement POST /auth/login endpoint in phase-2/backend/routes/auth.py (calls login service, returns JWT)
- [ ] T029 [US1] Register auth routes in phase-2/backend/main.py with /auth prefix

**Frontend Authentication UI:**

- [ ] T030 [P] [US1] Create phase-2/frontend/components/auth/RegisterForm.tsx with email/password inputs and validation
- [ ] T031 [P] [US1] Create phase-2/frontend/components/auth/LoginForm.tsx with email/password inputs
- [ ] T032 [P] [US1] Create phase-2/frontend/app/register/page.tsx using RegisterForm component
- [ ] T033 [P] [US1] Create phase-2/frontend/app/login/page.tsx using LoginForm component
- [ ] T034 [US1] Create phase-2/frontend/lib/auth-context.tsx with auth state provider (user, token, login, logout, register)
- [ ] T035 [US1] Wrap phase-2/frontend/app/layout.tsx with AuthProvider for app-wide auth state
- [ ] T036 [US1] Implement protected route middleware in phase-2/frontend/app/dashboard/layout.tsx (redirect if unauthenticated)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can register, login, receive JWT tokens, and access protected routes.

---

## Phase 4: User Story 2 - View Personal Task List (Priority: P1) 🎯 MVP

**Goal**: Display all user's tasks in a clear dashboard with user isolation enforced (no cross-user access)

**Independent Test**: Login as User A, create tasks, verify only their tasks appear. Login as User B, verify User A's tasks are not visible.

### Implementation for User Story 2

**Backend Task Listing:**

- [ ] T037 [US2] Create phase-2/backend/services/task_service.py with list_tasks(user_id) function filtering by authenticated user
- [ ] T038 [US2] Implement GET /api/{user_id}/tasks endpoint in phase-2/backend/routes/tasks.py (verify user_id matches JWT, call list_tasks service)
- [ ] T039 [US2] Register task routes in phase-2/backend/main.py with /api/{user_id}/tasks prefix and auth dependency

**Frontend Task List Display:**

- [ ] T040 [P] [US2] Create phase-2/frontend/services/task-service.ts with getTasks(userId) API call using api-client
- [ ] T041 [P] [US2] Create phase-2/frontend/components/tasks/TaskItem.tsx to display individual task (title, description, completed status)
- [ ] T042 [P] [US2] Create phase-2/frontend/components/tasks/TaskList.tsx to map tasks array to TaskItem components
- [ ] T043 [US2] Create phase-2/frontend/app/dashboard/page.tsx (protected route) fetching and displaying task list
- [ ] T044 [US2] Add empty state UI in phase-2/frontend/components/tasks/TaskList.tsx when no tasks exist
- [ ] T045 [P] [US2] Create phase-2/frontend/components/ui/LoadingSpinner.tsx for async operation loading states
- [ ] T046 [P] [US2] Create phase-2/frontend/components/ui/ErrorMessage.tsx for error state display
- [ ] T047 [US2] Add loading and error states to phase-2/frontend/app/dashboard/page.tsx

**Checkpoint**: Users can view their personal task list with proper user isolation. Tasks display correctly with empty, loading, and error states handled.

---

## Phase 5: User Story 3 - Create New Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks with title (required) and description (optional) that persist across sessions

**Independent Test**: Login, create task with title only, verify it appears. Create task with title+description, logout, login, verify tasks persist.

### Implementation for User Story 3

**Backend Task Creation:**

- [ ] T048 [US3] Implement create_task(user_id, title, description) function in phase-2/backend/services/task_service.py (set completed=false, timestamps)
- [ ] T049 [US3] Implement POST /api/{user_id}/tasks endpoint in phase-2/backend/routes/tasks.py (validate title 1-200 chars, description max 1000, call create_task)
- [ ] T050 [US3] Add request validation for title (required, 1-200 chars) and description (optional, max 1000) in phase-2/backend/routes/tasks.py

**Frontend Task Creation UI:**

- [ ] T051 [P] [US3] Create phase-2/frontend/components/tasks/TaskForm.tsx reusable form (title input, description textarea, submit/cancel buttons)
- [ ] T052 [P] [US3] Add form validation in phase-2/frontend/components/tasks/TaskForm.tsx (title required, length limits)
- [ ] T053 [P] [US3] Create phase-2/frontend/services/task-service.ts createTask(userId, data) API call
- [ ] T054 [US3] Create phase-2/frontend/app/tasks/new/page.tsx (protected route) using TaskForm for creation
- [ ] T055 [US3] Add "Add Task" or "New Task" button to phase-2/frontend/app/dashboard/page.tsx linking to /tasks/new
- [ ] T056 [US3] Add error handling for validation failures in phase-2/frontend/components/tasks/TaskForm.tsx

**Checkpoint**: Users can create tasks that persist to database. Title validation enforced, description optional. Tasks appear in list immediately after creation.

---

## Phase 6: User Story 4 - Update Existing Task (Priority: P2)

**Goal**: Enable users to edit task title and description with changes persisting to database

**Independent Test**: Create task, edit title, verify change persists. Edit description, verify change persists. Attempt to clear title, verify validation prevents it.

### Implementation for User Story 4

**Backend Task Update:**

- [ ] T057 [US4] Implement get_task(user_id, task_id) function in phase-2/backend/services/task_service.py (enforce ownership, return task or None)
- [ ] T058 [US4] Implement update_task(user_id, task_id, title, description) function in phase-2/backend/services/task_service.py (verify ownership, update fields, refresh updated_at)
- [ ] T059 [US4] Implement GET /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/routes/tasks.py (call get_task, return 404 if not found/not owned)
- [ ] T060 [US4] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/routes/tasks.py (validate payload, call update_task, return 404 if not owned)

**Frontend Task Update UI:**

- [ ] T061 [P] [US4] Add getTask(userId, taskId) and updateTask(userId, taskId, data) to phase-2/frontend/services/task-service.ts
- [ ] T062 [P] [US4] Create phase-2/frontend/app/tasks/[id]/edit/page.tsx (protected route) loading existing task data
- [ ] T063 [US4] Reuse phase-2/frontend/components/tasks/TaskForm.tsx in edit page with pre-filled data
- [ ] T064 [US4] Add "Edit" button to phase-2/frontend/components/tasks/TaskItem.tsx linking to /tasks/{id}/edit
- [ ] T065 [US4] Handle update success/failure in phase-2/frontend/app/tasks/[id]/edit/page.tsx (redirect to dashboard on success)

**Checkpoint**: Users can edit existing tasks. Changes persist correctly. Validation enforces title requirement. Only task owner can edit their tasks.

---

## Phase 7: User Story 5 - Mark Task as Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status with visual distinction between completed and incomplete tasks

**Independent Test**: Create task (incomplete), mark complete, verify status changes and persists. Toggle back to incomplete, verify change persists. Refresh page, verify status maintained.

### Implementation for User Story 5

**Backend Task Completion Toggle:**

- [ ] T066 [US5] Implement toggle_completion(user_id, task_id) function in phase-2/backend/services/task_service.py (flip completed boolean, update updated_at, enforce ownership)
- [ ] T067 [US5] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in phase-2/backend/routes/tasks.py (call toggle_completion, return updated task, 404 if not owned)

**Frontend Task Completion UI:**

- [ ] T068 [P] [US5] Add toggleComplete(userId, taskId) to phase-2/frontend/services/task-service.ts
- [ ] T069 [P] [US5] Add completion checkbox or button to phase-2/frontend/components/tasks/TaskItem.tsx
- [ ] T070 [US5] Implement toggle handler in phase-2/frontend/components/tasks/TaskItem.tsx (call toggleComplete, update UI optimistically)
- [ ] T071 [US5] Add visual styling in phase-2/frontend/components/tasks/TaskItem.tsx to distinguish completed tasks (strikethrough, different color, etc.)
- [ ] T072 [US5] Handle toggle errors in phase-2/frontend/components/tasks/TaskItem.tsx (revert UI on failure)

**Checkpoint**: Users can toggle task completion. Completed tasks are visually distinct. Status changes persist across page refreshes.

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Allow users to permanently delete tasks with confirmation to prevent accidental deletion

**Independent Test**: Create task, click delete, confirm deletion, verify task removed. Create task, click delete, cancel, verify task remains.

### Implementation for User Story 6

**Backend Task Deletion:**

- [ ] T073 [US6] Implement delete_task(user_id, task_id) function in phase-2/backend/services/task_service.py (verify ownership, delete from DB, return success boolean)
- [ ] T074 [US6] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/routes/tasks.py (call delete_task, return 204 No Content, 404 if not owned)

**Frontend Task Deletion UI:**

- [ ] T075 [P] [US6] Add deleteTask(userId, taskId) to phase-2/frontend/services/task-service.ts
- [ ] T076 [P] [US6] Create phase-2/frontend/components/tasks/DeleteConfirm.tsx modal/dialog with confirm/cancel buttons
- [ ] T077 [US6] Add "Delete" button to phase-2/frontend/components/tasks/TaskItem.tsx opening DeleteConfirm modal
- [ ] T078 [US6] Implement delete handler in phase-2/frontend/components/tasks/TaskItem.tsx (call deleteTask on confirm, remove from list)
- [ ] T079 [US6] Handle delete errors in phase-2/frontend/components/tasks/DeleteConfirm.tsx (show error message, keep modal open)

**Checkpoint**: Users can delete tasks with confirmation. Deletion is permanent. Cancelled deletions leave task unchanged. Task removed from list immediately after deletion.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, error handling, and production-readiness improvements

- [ ] T080 [P] Create phase-2/frontend/components/ui/Button.tsx reusable button component with consistent styling
- [ ] T081 [P] Create phase-2/frontend/components/ui/Input.tsx reusable input component with validation states
- [ ] T082 Add comprehensive error handling for 401 Unauthorized (redirect to login) in phase-2/frontend/lib/api-client.ts
- [ ] T083 Add comprehensive error handling for 403 Forbidden (user_id mismatch) in phase-2/frontend/lib/api-client.ts
- [ ] T084 Add loading states to all async operations in phase-2/frontend/app/dashboard/page.tsx
- [ ] T085 [P] Implement responsive design for mobile (320px width minimum) in phase-2/frontend/app/dashboard/page.tsx
- [ ] T086 [P] Add better-auth JWT token refresh logic in phase-2/frontend/lib/auth.ts
- [ ] T087 Verify all database queries in phase-2/backend/services/task_service.py filter by user_id (security audit)
- [ ] T088 Add input sanitization for XSS prevention in phase-2/backend/routes/tasks.py and phase-2/backend/routes/auth.py
- [ ] T089 Test with 100 tasks per user to verify performance meets < 2 second load target
- [ ] T090 Run manual E2E validation following specs/001-fullstack-web-app/quickstart.md (all 8 test scenarios)
- [ ] T091 Update phase-2/README.md with setup instructions from quickstart.md
- [ ] T092 Verify Phase II constitutional compliance (stateless auth, user isolation, no AI/MCP, spec-driven)

**Checkpoint**: All user stories complete, polished, and production-ready. Manual E2E validation passed.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent (only needs Task model from foundational)
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Independent (only needs Task model from foundational)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent (reuses GET endpoint from US2, adds PUT)
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Independent (adds PATCH endpoint)
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - Independent (adds DELETE endpoint)

### Within Each User Story

- Backend services before backend routes
- Backend routes before frontend services
- Frontend services before frontend UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T007, T008, T011, T012 can run in parallel (different directories/files)

**Phase 2 (Foundational)**: T022, T023 can run in parallel (frontend types, no dependencies)

**User Story 1**:
- T024, T025, T026 can run in parallel (backend services, same file but different functions)
- T030, T031, T032, T033 can run in parallel (frontend components/pages, different files)

**User Story 2**:
- T040, T041, T042, T045, T046 can run in parallel (frontend components/services, different files)

**User Story 3**:
- T051, T052, T053 can run in parallel (frontend form component and service, different files)

**User Story 4**:
- T061, T062 can run in parallel (frontend service and page, different files)

**User Story 5**:
- T068, T069 can run in parallel (frontend service and component, different files)

**User Story 6**:
- T075, T076 can run in parallel (frontend service and component, different files)

**Phase 9 (Polish)**:
- T080, T081, T085, T086 can run in parallel (frontend UI components and features, different files)

**Once Foundational phase completes, all user stories (Phase 3-8) can start in parallel (if team capacity allows)**

---

## Parallel Example: User Story 1

```bash
# Launch all parallelizable backend services for User Story 1 together:
Task: "Create auth_service.py with password hashing"
Task: "Implement user registration service"
Task: "Implement user login service"

# Launch all parallelizable frontend components for User Story 1 together:
Task: "Create RegisterForm.tsx"
Task: "Create LoginForm.tsx"
Task: "Create register page"
Task: "Create login page"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only - All P1)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (View Tasks)
5. Complete Phase 5: User Story 3 (Create Tasks)
6. **STOP and VALIDATE**: Test User Stories 1-3 independently (MVP complete!)
7. Deploy/demo if ready

**MVP delivers**: User registration, login, task viewing, and task creation - a complete working todo application.

### Incremental Delivery (Add P2 and P3 Stories)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently
3. Add User Story 2 → Test independently
4. Add User Story 3 → Test independently → **MVP deployed!**
5. Add User Story 4 (Update) → Test independently → Deploy
6. Add User Story 5 (Complete) → Test independently → Deploy
7. Add User Story 6 (Delete) → Test independently → Deploy
8. Phase 9: Polish → Final deployment

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (View Tasks)
   - Developer C: User Story 3 (Create Tasks)
3. After P1 stories complete:
   - Developer A: User Story 4 (Update Tasks)
   - Developer B: User Story 5 (Mark Complete)
   - Developer C: User Story 6 (Delete Tasks)
4. Team collaborates on Phase 9: Polish

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
- Follow specs/001-fullstack-web-app/quickstart.md for E2E validation scenarios
- Commit after each task or logical group
- All paths use monorepo structure: phase-2/backend/ and phase-2/frontend/
- No tests in this phase (manual E2E validation only)
- Security: All backend queries MUST filter by authenticated user_id
- Authentication: JWT required on all API endpoints (except /auth/register and /auth/login)
- Validation: Title 1-200 chars (required), Description max 1000 chars (optional)
- Forward compatibility: Maintain stateless architecture for Phase III AI agent integration

---

**Total Tasks**: 92
**Parallelizable Tasks**: 28 marked with [P]
**User Stories**: 6 (3 P1, 2 P2, 1 P3)
**MVP Scope**: User Stories 1, 2, 3 (Phases 1-5: 56 tasks)
**Full Scope**: All 6 User Stories (Phases 1-9: 92 tasks)
