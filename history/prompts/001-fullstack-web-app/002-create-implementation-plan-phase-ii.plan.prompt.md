---
id: 002
title: Create Implementation Plan Phase II
stage: plan
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: fullstack-web-app
branch: 001-fullstack-web-app
user: user
command: /sp.plan
labels: ["implementation-plan", "architecture", "7-layer-strategy", "better-auth", "jwt", "rest-api", "nextjs", "fastapi", "monorepo"]
links:
  spec: specs/001-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fullstack-web-app/plan.md
  - specs/001-fullstack-web-app/contracts/data-models.md
  - specs/001-fullstack-web-app/contracts/api-endpoints.md
  - specs/001-fullstack-web-app/contracts/auth-flow.md
  - specs/001-fullstack-web-app/quickstart.md
tests:
  - N/A (planning phase)
---

## Prompt

Transform the Phase I console-based Todo application into a full-stack web application following a 7-layer execution strategy:

**Execution Strategy Overview**:
1. Monorepo & Spec-Kit initialization
2. Backend infrastructure foundation
3. Authentication integration (Better Auth + JWT)
4. Task domain + persistence
5. REST API enforcement
6. Frontend foundation
7. Frontend integration + validation

Each layer must be completed and validated before moving to the next.

**Technology Stack**:
- Frontend: Next.js 16+ (App Router), Better Auth, TypeScript, Tailwind CSS
- Backend: FastAPI (Python 3.13+), SQLModel, JWT verification
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (frontend) + JWT verification (backend)
- Architecture: Stateless, RESTful, clean API boundaries

**Key Requirements**:
- Multi-user support with JWT authentication
- User isolation (100% data filtering by user_id)
- RESTful API with user_id in URL path
- 5 core operations: Add, View, Update, Delete, Mark Complete
- Stateless architecture for Phase III extensibility
- Monorepo structure following Spec-Kit Plus compliance

**Security Model**:
- JWT required on all API endpoints
- Backend verifies JWT signature using shared BETTER_AUTH_SECRET
- URL user_id must match JWT user_id (403 Forbidden if mismatch)
- All database queries filtered by authenticated user_id
- No cross-user data access allowed

**Project Structure**:
```
phase-2/
├── backend/        # FastAPI with core/, models/, routes/, services/
└── frontend/       # Next.js with app/, components/, lib/, services/
```

**Performance Targets**:
- User registration: < 1 minute
- Login: < 10 seconds
- Task operations: < 15 seconds (create), < 3 seconds (update/delete/complete)
- Task list load: < 2 seconds
- Concurrent users: 100+ without degradation

**Forward Compatibility**:
- Stateless design (no server sessions)
- Clean REST boundaries for AI agent consumption (Phase III)
- Extensible data model (Task and User entities)
- Loose coupling between frontend and backend

## Response snapshot

Created comprehensive implementation plan with 8 implementation layers and complete Phase 1 design documentation.

**Plan Components**:
- **Summary**: Transform console app to multi-user web app using Next.js + FastAPI + Neon PostgreSQL
- **Technical Context**: Python 3.13+, TypeScript 5.x, Next.js 16+, FastAPI, SQLModel, Better Auth, Neon PostgreSQL
- **Constitution Check**: All compliance criteria met (spec-driven, phase compliance, tech stack, structure, clean code)
- **Project Structure**: Monorepo with phase-2/backend/ and phase-2/frontend/, comprehensive directory trees defined
- **Implementation Layers (8)**:
  - Layer 0: Monorepo & Spec-Kit initialization
  - Layer 1: Backend foundation (FastAPI setup, DB connection)
  - Layer 2: Authentication integration (Better Auth + JWT verification)
  - Layer 3: Task domain & persistence (SQLModel, service layer, user filtering)
  - Layer 4: REST API enforcement (6 endpoints with security)
  - Layer 5: Frontend foundation (Next.js setup, API client)
  - Layer 6: Frontend authentication flow (login, register, protected routes)
  - Layer 7: Frontend task workflows (CRUD UI components)
  - Layer 8: Integration & hardening (E2E testing, security validation)

**Phase 1 Design Documents Created**:

1. **contracts/data-models.md** (273 lines):
   - User entity (Better Auth managed): id (UUID), email, created_at
   - Task entity (backend managed): id, user_id, title, description, completed, created_at, updated_at
   - TypeScript and Python type definitions
   - Database schema (SQL)
   - Validation rules and constraints
   - Edge cases handling

2. **contracts/api-endpoints.md** (411 lines):
   - 6 REST endpoints with complete specifications
   - GET /api/{user_id}/tasks - List user tasks
   - POST /api/{user_id}/tasks - Create task
   - GET /api/{user_id}/tasks/{id} - Get single task
   - PUT /api/{user_id}/tasks/{id} - Update task
   - DELETE /api/{user_id}/tasks/{id} - Delete task
   - PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion
   - Request/response examples with curl commands
   - Error response specifications (401, 403, 404, 400, 500)
   - Security guarantees and performance characteristics

3. **contracts/auth-flow.md** (579 lines):
   - JWT token structure (header, payload, signature)
   - 4 authentication flows with sequence diagrams:
     - User registration flow
     - User login flow
     - Authenticated API request flow
     - Token expiration & refresh flow
   - Backend JWT verification implementation (pseudocode)
   - Frontend token storage strategies (httpOnly cookies vs localStorage)
   - Security considerations (shared secret, expiration, HTTPS, CORS, user ID verification)
   - Environment variables configuration
   - Testing authentication (manual and automated)

4. **quickstart.md** (378 lines):
   - Prerequisites (Python 3.13+, Node.js 20+, Neon account)
   - Step-by-step setup instructions (backend and frontend)
   - Environment variable configuration
   - Database initialization
   - 8 first-run tests (register, login, create task, view, complete, edit, delete, user isolation)
   - Troubleshooting guide (backend, frontend, authentication issues)
   - Development workflow
   - Common commands reference

**Risk Analysis**:
- Identified 10 risks with mitigations
- JWT secret mismatch → shared env var
- Cross-user data access → service layer filtering validation
- Tight coupling → strict API contract adherence
- Neon connection issues → early testing, clear errors
- Better Auth version incompatibility → pinned versions
- Token storage security → httpOnly cookies
- Database migration complexity → manual migrations, version control
- CORS misconfiguration → Layer 2 early testing
- Performance degradation → no pagination Phase II (acceptable)
- Spec drift → always reference specs, create ADRs

**ADR Candidates Identified (4)**:
1. Authentication Architecture: Better Auth + JWT (after Layer 2)
2. Data Isolation Strategy: Service Layer User Filtering (after Layer 3)
3. API Contract: RESTful with User ID in URL (after Layer 4)
4. Frontend Architecture: Next.js App Router with Client Components (after Layer 5)

**Files Created**:
- specs/001-fullstack-web-app/plan.md (359 lines)
- specs/001-fullstack-web-app/contracts/data-models.md (273 lines)
- specs/001-fullstack-web-app/contracts/api-endpoints.md (411 lines)
- specs/001-fullstack-web-app/contracts/auth-flow.md (579 lines)
- specs/001-fullstack-web-app/quickstart.md (378 lines)

**Total**: 2,000 lines of comprehensive planning and design documentation

## Outcome

- ✅ Impact: Complete architectural plan defining 8 implementation layers with concrete technical decisions; establishes stateless JWT authentication, service-layer user isolation, and RESTful API patterns; creates foundation for Phase III AI agent integration
- 🧪 Tests: Layer validation checkpoints defined for each of 8 layers; E2E test scenarios documented (8 first-run tests in quickstart); security validation tests specified
- 📁 Files: Created plan.md, 4 contract documents (data-models, api-endpoints, auth-flow, quickstart); total 2,000 lines; all documents cross-referenced
- 🔁 Next prompts: /sp.tasks (generate actionable tasks from plan), /sp.adr <title> (create ADRs after completing layers 2-5)
- 🧠 Reflection: Plan successfully balances technical precision with implementation practicality; 7-layer strategy ensures incremental validation; Better Auth + JWT architecture enables stateless design for Phase III; service-layer filtering provides robust user isolation without database complexity; comprehensive contracts enable parallel frontend/backend development

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all required artifacts
- Graders run and results (PASS/FAIL): Plan completeness PASSED (8 layers defined, validation criteria specified, risks identified); Constitutional compliance PASSED (all criteria met); Contract completeness PASSED (4 complete design documents); ADR identification PASSED (4 significant decisions identified)
- Prompt variant (if applicable): Standard /sp.plan workflow with user-provided 7-layer execution strategy integrated into plan template structure
- Next experiment (smallest change to try): Execute /sp.tasks to convert plan into actionable tasks; validate that Layer 0-8 sequence translates cleanly into dependency-ordered tasks with acceptance criteria
