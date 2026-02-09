---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-02-08
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, governance, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
# Evolution of Todo — Project Constitution

---

## Todo App Feature Progression

### Basic Level (Core Essentials)

These form the foundation—quick to build, essential for any MVP:
1. Add Task – Create new todo items
2. Delete Task – Remove tasks from the list
3. Update Task – Modify existing task details
4. View Task List – Display all tasks
5. Mark as Complete – Toggle task completion status

### Intermediate Level (Organization & Usability)

Add these to make the app feel polished and practical:
1. Priorities & Tags/Categories – Assign levels (high/medium/low) or labels (work/home)
3. Search & Filter – Search by keyword; filter by status, priority, or date
4. Sort Tasks – Reorder by due date, priority, or alphabetically

### Advanced Level (Intelligent Features)

1. Recurring Tasks – Auto-reschedule repeating tasks (e.g., "weekly meeting")
2. Due Dates & Time Reminders – Set deadlines with date/time pickers; browser notifications

Use Agentic Dev Stack for building this hackathon project.

---

## 1. Purpose & Vision

This project represents the **end-to-end evolution of software systems**:

**CLI → Web → AI Agent → Kubernetes → Cloud-Native Event-Driven Architecture**

The goal is to train developers as **Product Architects**, not manual coders.
All development is **spec-driven, AI-executed, and architecture-first**.

---

## 2. Absolute Rules (Non-Negotiable)

1. **Spec-Driven Development Only**
   - No feature without a specification
   - No implementation without a plan
   - No manual coding by humans

## 3. Repository & Folder Law

- Each phase lives in its **own folder**
- Constitution is **shared across all phases**
- Specs must be versioned and preserved
- No orphan code without specs

Hackathon-II-Todo-Spec-Driven-Dev-and-Cloud-Native-AI/
├── phase-1/
├── phase-2/
├── phase-3/
├── phase-4/
├── phase-5/
├── specs/
├── .spec-kit/
├── CLAUDE.md
└── README.md


---

## 4. Code Quality Standards

- Simple and readable code
- Clean functions and modules
- Minimal abstractions
- Explicit naming
- GitHub-quality structure
- MCP Context-7 inspired clarity

---

## 5. Phase Constraints

### Phase I — In-Memory Console App
**Python · CLI · In-Memory Only**


### Purpose
- Build a CLI-based Todo app that stores tasks in memory.

### Rules & Principles
- All task operations must be in-memory (no database).
- Follow **clean code**: clear functions, modular design, readable code.
- Implement using **Claude Code only**; no manual coding.
- Each feature must have spec, plan, tasks, and implementation.

### Technology Stack:
- UV package manager
- Python 3.13+

### Standards
- Python 3.13+
- Project structure: `/src`, `/specs`, `/README.md`, `/CLAUDE.md`
- Task model: `id`, `title`, `description`, `completed`, `created_at`
- CLI commands: Add, Delete, Update, View, Mark Complete
- All features must confirm actions via console output.

- No database
- No persistence
- Basic CRUD features only


---

### Phase II — Full-Stack Web Application
**Next.js · FastAPI · Neon PostgreSQL**


### Purpose
- Transform CLI Todo app into a full-stack web app with persistent storage.
- Implement multi-user support and JWT authentication via Better Auth.

### Rules & Principles
- Use **Next.js 16+ (App Router)** for frontend and **FastAPI** for backend.
- Use **SQLModel + Neon DB** for persistence.
- RESTful endpoints under `/api/{user_id}/tasks`.
- JWT authentication required for all endpoints.
- Claude Code and Spec-Kit Plus required for all code generation.
- Follow **clean architecture**: separate frontend, backend, and specs.

### Standards
- Frontend: TypeScript, Tailwind CSS, server/client components
- Backend: Pydantic models, SQLModel ORM, structured routes
- API endpoints must handle user isolation and validation
- Monorepo layout: `/frontend`, `/backend`, `/specs`
- Spec-driven workflow mandatory for all features

- REST APIs only
- JWT-based authentication
- Strict user data isolation
- Business logic stays in backend
- Frontend consumes APIs only

---

### Phase III — AI-Powered Todo Chatbot
**OpenAI ChatKit · Agents SDK · MCP**

### Purpose
- Implement AI-driven chatbot interface for managing tasks via natural language.
- Integrate OpenAI ChatKit, Agents SDK, and MCP tools.
- Reuse Phase II app as backend for chatbot features.

### Rules & Principles
- Chatbot must handle all **Basic Level Todo features**.
- AI agents use MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`.
- Server is **stateless**; conversation history stored in DB.
- Multi-language support (Urdu) and optional voice input.
- Follow clean Python + TypeScript code standards.

### Standards
- FastAPI backend exposes `/api/{user_id}/chat`
- Use OpenAI Agents SDK for AI behavior
- MCP server tools must follow defined input/output schemas
- Frontend ChatKit UI must confirm all actions
- All implementations strictly spec-driven


- All task operations exposed as MCP tools
- AI must use tools — no direct DB access
- Stateless backend
- Conversation state stored in database
- Multi-language support (English + Urdu)

---

### Phase IV — Local Kubernetes Deployment
**Docker · Minikube · Helm · kubectl-ai**


### Purpose
- Deploy Phase III Todo Chatbot locally using Minikube and Helm.
- Introduce containerization and AI-assisted DevOps.

### Rules & Principles
- Containerize frontend and backend using Docker.
- Use **Helm charts** for deployment.
- AI-assisted Kubernetes operations via `kubectl-ai` and `kagent`.
- Maintain stateless design; no local changes should break AI operations.
- Keep all containers and charts version-controlled.

### Standards
- Minikube cluster with multiple replicas for frontend/backend
- Standardized Dockerfile structure and naming conventions
- Monitor pods and logs via Helm and kubectl
- Apply Spec-Kit Plus workflow for infra and app deployment
- All YAML manifests and charts tracked in repo

- All services containerized
- Helm charts required
- No hardcoded secrets
- Local cluster must be reproducible

---

### Phase V — Cloud-Native & Event-Driven System
**Kafka · Dapr · Managed Kubernetes**


### Purpose
- Deploy fully-featured Todo Chatbot with advanced cloud-native architecture.
- Introduce event-driven architecture (Kafka), Dapr, CI/CD, monitoring, and cloud deployment.

### Rules & Principles
- Implement all **Intermediate + Advanced features**:
  - Priorities, Tags, Search, Filter, Sort
  - Recurring tasks, Due dates, Reminders
- Use **Kafka** for events, Dapr for distributed microservices
- Deploy to Minikube first, then Azure AKS / GKE / Oracle OKE
- CI/CD via GitHub Actions
- Deployments must be reproducible from Spec-Kit Plus specs

### Standards
- Kafka topics: `task-events`, `reminders`, `task-updates`
- Dapr sidecars handle Pub/Sub, state, cron bindings
- Kubernetes manifests and Helm charts must be clean and modular
- Monitoring/logging enabled via standard tools
- All specs, plans, and tasks updated in `/specs`


- Event-driven architecture mandatory
- Kafka for async workflows
- Dapr abstract
```

## Response snapshot

Constitution file updated successfully with the following content:

# Todo Spec Driven Dev and Cloud Native AI Constitution

## Core Principles

### Spec-Driven Development Only
All development follows the spec-driven approach: No feature without a specification, No implementation without a plan, No manual coding by humans. This ensures architectural discipline and traceability from requirements to implementation.

### Agentic Development Stack
Use AI agents for all development tasks following the evolution path: CLI → Web → AI Agent → Kubernetes → Cloud-Native Event-Driven Architecture. This trains developers as Product Architects, not manual coders.

### Phase-Based Architecture Evolution
Development progresses through distinct phases with specific constraints and technology stacks, maintaining clear separation of concerns and enabling systematic complexity growth from simple in-memory apps to sophisticated cloud-native systems.

### Repository Organization Law
Each phase lives in its own folder with shared constitution, specs must be versioned and preserved, and no orphan code without specs. This ensures clean separation and traceability across the evolution path.

### Clean Code Standards
Maintain simple and readable code, clean functions and modules, minimal abstractions, explicit naming, GitHub-quality structure, and MCP Context-7 inspired clarity across all implementations.

### Technology Stack Adherence
Each phase has specific technology constraints that must be followed: Phase I (Python CLI, In-Memory), Phase II (Next.js/FastAPI/Neon), Phase III (OpenAI/Agents/MCP), Phase IV (Docker/Kubernetes/Helm), Phase V (Kafka/Dapr/Event-Driven).

## Phase Constraints and Standards

### Phase I — In-Memory Console App (Python · CLI · In-Memory Only)
Build a CLI-based Todo app that stores tasks in memory. All task operations must be in-memory (no database), follow clean code principles with clear functions, modular design, and readable code. Implement using Claude Code only; no manual coding. Each feature must have spec, plan, tasks, and implementation. Technology stack: UV package manager, Python 3.13+. Standards: Python 3.13+, project structure with `/src`, `/specs`, `/README.md`, `/CLAUDE.md`, task model with `id`, `title`, `description`, `completed`, `created_at`, CLI commands for Add, Delete, Update, View, Mark Complete. Constraints: No database, no persistence, Basic CRUD features only.

### Phase II — Full-Stack Web Application (Next.js · FastAPI · Neon PostgreSQL)
Transform CLI Todo app into a full-stack web app with persistent storage. Implement multi-user support and JWT authentication via Better Auth. Use Next.js 16+ (App Router) for frontend and FastAPI for backend. Use SQLModel + Neon DB for persistence. RESTful endpoints under `/api/{user_id}/tasks`. JWT authentication required for all endpoints. Claude Code and Spec-Kit Plus required for all code generation. Follow clean architecture: separate frontend, backend, and specs. Standards: Frontend (TypeScript, Tailwind CSS, server/client components), Backend (Pydantic models, SQLModel ORM, structured routes), API endpoints must handle user isolation and validation, Monorepo layout: `/frontend`, `/backend`, `/specs`. Constraints: REST APIs only, JWT-based authentication, strict user data isolation, business logic stays in backend, frontend consumes APIs only.

### Phase III — AI-Powered Todo Chatbot (OpenAI ChatKit · Agents SDK · MCP)
Implement AI-driven chatbot interface for managing tasks via natural language. Integrate OpenAI ChatKit, Agents SDK, and MCP tools. Reuse Phase II app as backend for chatbot features. Chatbot must handle all Basic Level Todo features. AI agents use MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`. Server is stateless; conversation history stored in DB. Multi-language support (Urdu) and optional voice input. Follow clean Python + TypeScript code standards. Standards: FastAPI backend exposes `/api/{user_id}/chat`, Use OpenAI Agents SDK for AI behavior, MCP server tools must follow defined input/output schemas, Frontend ChatKit UI must confirm all actions. Constraints: All task operations exposed as MCP tools, AI must use tools — no direct DB access, stateless backend, conversation state stored in database, multi-language support (English + Urdu).

### Phase IV — Local Kubernetes Deployment (Docker · Minikube · Helm · kubectl-ai)
Deploy Phase III Todo Chatbot locally using Minikube and Helm. Introduce containerization and AI-assisted DevOps. Containerize frontend and backend using Docker. Use Helm charts for deployment. AI-assisted Kubernetes operations via kubectl-ai and kagent. Maintain stateless design; no local changes should break AI operations. Keep all containers and charts version-controlled. Standards: Minikube cluster with multiple replicas for frontend/backend, Standardized Dockerfile structure and naming conventions, Monitor pods and logs via Helm and kubectl, Apply Spec-Kit Plus workflow for infra and app deployment. Constraints: All services containerized, Helm charts required, No hardcoded secrets, Local cluster must be reproducible.

### Phase V — Cloud-Native & Event-Driven System (Kafka · Dapr · Managed Kubernetes)
Deploy fully-featured Todo Chatbot with advanced cloud-native architecture. Introduce event-driven architecture (Kafka), Dapr, CI/CD, monitoring, and cloud deployment. Implement all Intermediate + Advanced features: Priorities, Tags, Search, Filter, Sort, Recurring tasks, Due dates, Reminders. Use Kafka for events, Dapr for distributed microservices. Deploy to Minikube first, then Azure AKS / GKE / Oracle OKE. CI/CD via GitHub Actions. Deployments must be reproducible from Spec-Kit Plus specs. Standards: Kafka topics (`task-events`, `reminders`, `task-updates`), Dapr sidecars handle Pub/Sub, state, cron bindings, Kubernetes manifests and Helm charts must be clean and modular, Monitoring/logging enabled via standard tools. Constraints: Event-driven architecture mandatory, Kafka for async workflows, Dapr abstraction required.

## Development Workflow

All development follows the Spec-Kit Plus workflow: Create specification → Generate plan → Generate tasks → Implement using Claude Code → Create Prompt History Records (PHRs) for all activities → Document Architectural Decision Records (ADRs) for significant decisions. Each phase must be completed before moving to the next, with proper handoff artifacts and compliance checks.

## Governance

This constitution governs all development activities and supersedes any conflicting practices. Amendments require documentation of the change, approval from project maintainers, and a migration plan for existing work. All implementations must comply with the phase-specific constraints and technology stacks defined herein. Code reviews must verify constitutional compliance, and complexity must be justified against simpler alternatives. Use CLAUDE.md for detailed runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08

## Outcome

- ✅ Impact: Created project constitution with 5-phase architecture and clear development guidelines
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with complete constitution
- 🔁 Next prompts: Ready for feature specification using /sp.specify
- 🧠 Reflection: Constitution provides clear framework for the entire evolution path from CLI to cloud-native

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard constitution update
- Next experiment (smallest change to try): Begin with Phase I feature specification