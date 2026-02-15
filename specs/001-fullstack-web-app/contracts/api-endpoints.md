# API Endpoints: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Created**: 2026-02-12
**Status**: Design Phase

## Overview

This document defines the REST API contract for the Phase II multi-user todo application backend. All endpoints require JWT authentication and enforce user isolation.

## Base Configuration

**Base URL**: `http://localhost:8000/api`

**Authentication**: All endpoints require JWT token in Authorization header
```http
Authorization: Bearer <JWT_TOKEN>
```

**Content Type**: `application/json` (for request/response bodies)

**CORS**: Allow origin `http://localhost:3000` (frontend development server)

## Global Error Responses

All endpoints may return these error responses:

### 401 Unauthorized
**Cause**: Missing, invalid, or expired JWT token

```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
**Cause**: user_id in URL doesn't match JWT user_id

```json
{
  "detail": "Forbidden: user_id mismatch"
}
```

### 500 Internal Server Error
**Cause**: Unexpected server error

```json
{
  "detail": "Internal server error"
}
```

## Endpoints

### 1. List User Tasks

Retrieve all tasks owned by the authenticated user.

```http
GET /api/{user_id}/tasks
```

**Path Parameters**:
- `user_id` (string, required): UUID of the user (must match JWT user_id)

**Headers**:
```http
Authorization: Bearer <JWT_TOKEN>
```

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
    },
    {
      "id": 2,
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Write documentation",
      "description": null,
      "completed": true,
      "createdAt": "2026-02-12T09:00:00Z",
      "updatedAt": "2026-02-12T10:30:00Z"
    }
  ]
}
```

**Notes**:
- Returns empty array if user has no tasks
- Tasks are ordered by created_at descending (newest first)
- No pagination for Phase II

---

### 2. Create Task

Create a new task for the authenticated user.

```http
POST /api/{user_id}/tasks
```

**Path Parameters**:
- `user_id` (string, required): UUID of the user (must match JWT user_id)

**Headers**:
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Field Validation**:
- `title` (string, required): 1-200 characters
- `description` (string, optional): max 1000 characters; omit or set to null for no description

**Response** (201 Created):
```json
{
  "id": 3,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "New task title",
  "description": "Optional task description",
  "completed": false,
  "createdAt": "2026-02-12T11:00:00Z",
  "updatedAt": "2026-02-12T11:00:00Z"
}
```

**Error Responses**:

**400 Bad Request** (validation error):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**Example validation errors**:
- Title missing: `"field required"`
- Title empty: `"ensure this value has at least 1 characters"`
- Title too long (>200): `"ensure this value has at most 200 characters"`
- Description too long (>1000): `"ensure this value has at most 1000 characters"`

---

### 3. Get Single Task

Retrieve details of a specific task owned by the authenticated user.

```http
GET /api/{user_id}/tasks/{task_id}
```

**Path Parameters**:
- `user_id` (string, required): UUID of the user (must match JWT user_id)
- `task_id` (integer, required): ID of the task

**Headers**:
```http
Authorization: Bearer <JWT_TOKEN>
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

**404 Not Found**:
```json
{
  "detail": "Task not found"
}
```

**Causes**:
- Task ID doesn't exist
- Task exists but belongs to a different user

---

### 4. Update Task

Update title and/or description of an existing task owned by the authenticated user.

```http
PUT /api/{user_id}/tasks/{task_id}
```

**Path Parameters**:
- `user_id` (string, required): UUID of the user (must match JWT user_id)
- `task_id` (integer, required): ID of the task

**Headers**:
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated description"
}
```

**Field Validation**:
- `title` (string, required): 1-200 characters
- `description` (string, optional): max 1000 characters; set to null to clear description

**Response** (200 OK):
```json
{
  "id": 1,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": false,
  "createdAt": "2026-02-12T10:00:00Z",
  "updatedAt": "2026-02-12T11:15:00Z"
}
```

**Notes**:
- `updatedAt` timestamp is automatically refreshed
- `completed` status is NOT modified by this endpoint (use PATCH /complete for that)

**Error Responses**:
- **400 Bad Request**: Validation errors (same as Create Task)
- **404 Not Found**: Task doesn't exist or belongs to different user

---

### 5. Delete Task

Permanently delete a task owned by the authenticated user.

```http
DELETE /api/{user_id}/tasks/{task_id}
```

**Path Parameters**:
- `user_id` (string, required): UUID of the user (must match JWT user_id)
- `task_id` (integer, required): ID of the task

**Headers**:
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response** (204 No Content):
- Empty response body
- HTTP status 204 indicates successful deletion

**Error Responses**:
- **404 Not Found**: Task doesn't exist or belongs to different user

**Notes**:
- Deletion is permanent (no soft delete in Phase II)
- No confirmation required at API level (frontend handles confirmation UI)

---

### 6. Toggle Task Completion

Toggle the completion status of a task (incomplete → complete or complete → incomplete).

```http
PATCH /api/{user_id}/tasks/{task_id}/complete
```

**Path Parameters**:
- `user_id` (string, required): UUID of the user (must match JWT user_id)
- `task_id` (integer, required): ID of the task

**Headers**:
```http
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**: Empty (no body required)

**Response** (200 OK):
```json
{
  "id": 1,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete project",
  "description": "Finish Phase II implementation",
  "completed": true,
  "createdAt": "2026-02-12T10:00:00Z",
  "updatedAt": "2026-02-12T11:30:00Z"
}
```

**Notes**:
- Toggles between true and false (idempotent operation)
- If currently incomplete, sets to complete
- If currently complete, sets to incomplete
- `updatedAt` timestamp is automatically refreshed

**Error Responses**:
- **404 Not Found**: Task doesn't exist or belongs to different user

---

## Request/Response Examples

### Example 1: Create and Complete a Task

**Step 1: Create Task**
```bash
curl -X POST http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/tasks \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Review code", "description": "Review PR #42"}'
```

Response:
```json
{
  "id": 5,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Review code",
  "description": "Review PR #42",
  "completed": false,
  "createdAt": "2026-02-12T12:00:00Z",
  "updatedAt": "2026-02-12T12:00:00Z"
}
```

**Step 2: Mark Complete**
```bash
curl -X PATCH http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/tasks/5/complete \
  -H "Authorization: Bearer eyJhbGc..."
```

Response:
```json
{
  "id": 5,
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Review code",
  "description": "Review PR #42",
  "completed": true,
  "createdAt": "2026-02-12T12:00:00Z",
  "updatedAt": "2026-02-12T12:05:00Z"
}
```

### Example 2: Unauthorized Access

**Attempt to access another user's task**
```bash
curl -X GET http://localhost:8000/api/different-user-id/tasks \
  -H "Authorization: Bearer eyJhbGc..."
```

Response (403 Forbidden):
```json
{
  "detail": "Forbidden: user_id mismatch"
}
```

### Example 3: Invalid Token

**Request without Authorization header**
```bash
curl -X GET http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/tasks
```

Response (401 Unauthorized):
```json
{
  "detail": "Could not validate credentials"
}
```

## Security Guarantees

1. **JWT Validation**: All endpoints validate JWT signature and expiration
2. **User ID Verification**: URL user_id must match JWT `sub` claim
3. **Data Isolation**: All queries filtered by authenticated user_id
4. **No Cross-User Access**: User A cannot read/modify User B's tasks under any circumstances
5. **Stateless**: No server-side session storage; all auth via JWT

## Performance Characteristics

- **List Tasks**: O(n) where n = number of user's tasks; optimized by user_id index
- **Create Task**: O(1) constant time
- **Get Task**: O(1) constant time (primary key lookup)
- **Update Task**: O(1) constant time
- **Delete Task**: O(1) constant time
- **Toggle Complete**: O(1) constant time

**Expected Response Times** (Phase II targets):
- Simple queries (get, create, update, delete, toggle): < 200ms p95
- List tasks (up to 100 tasks): < 500ms p95

## Future Enhancements (Phase III+)

- **Pagination**: Add `?page=1&limit=20` query parameters to List Tasks
- **Filtering**: Add `?completed=true` query parameter to filter by status
- **Sorting**: Add `?sort=title&order=asc` query parameters
- **Search**: Add `?q=keyword` query parameter for title/description search
- **Bulk Operations**: POST `/api/{user_id}/tasks/bulk` for batch create/update/delete
- **Task Sharing**: POST `/api/{user_id}/tasks/{id}/share` to grant access to other users
- **Versioning**: Add `/v1/` prefix for API versioning (`/api/v1/{user_id}/tasks`)
