# Authentication Flow: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Created**: 2026-02-12
**Status**: Design Phase

## Overview

This document defines the authentication architecture for the Phase II multi-user todo application, using Better Auth for frontend authentication and JWT verification in the backend.

## Architecture Principles

1. **Stateless Authentication**: No server-side session storage; all state in JWT tokens
2. **Frontend-Issued Tokens**: Better Auth handles user registration/login and issues JWTs
3. **Backend Verification**: FastAPI verifies JWT signature and enforces authorization
4. **Shared Secret**: Both frontend and backend use `BETTER_AUTH_SECRET` for JWT signing/verification
5. **User Isolation**: Every API request is filtered by authenticated user_id

## Components

### Frontend (Next.js + Better Auth)
- Handles user registration UI
- Handles login UI
- Issues JWT tokens upon successful authentication
- Stores tokens securely (httpOnly cookies recommended)
- Attaches tokens to API requests (Authorization header)
- Handles token refresh/expiration

### Backend (FastAPI)
- Validates JWT signature using shared secret
- Extracts user_id from JWT payload
- Verifies URL user_id matches token user_id
- Filters all database queries by authenticated user_id
- Returns 401/403 for invalid/unauthorized requests

### Database (Neon PostgreSQL)
- Stores user accounts (managed by Better Auth)
- Stores tasks with user_id foreign key
- No authentication logic (handled by application layer)

## JWT Token Structure

### Token Format

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNlNDU2Ny1lODliLTEyZDMtYTQ1Ni00MjY2MTQxNzQwMDAiLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJpYXQiOjE3MDc3MzkyMDAsImV4cCI6MTcwNzgyNTYwMH0.signature
```

### Decoded Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Decoded Payload

```json
{
  "sub": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "iat": 1707739200,
  "exp": 1707825600
}
```

**Claims**:
- `sub` (Subject): User ID (UUID) - **PRIMARY IDENTIFIER** for authorization
- `email`: User email address (for display/reference)
- `iat` (Issued At): Timestamp when token was issued
- `exp` (Expiration): Timestamp when token expires

**Signature**:
- Algorithm: HMAC-SHA256 (HS256)
- Secret: `BETTER_AUTH_SECRET` environment variable (must match frontend/backend)

## Authentication Flows

### 1. User Registration Flow

```
User                  Frontend (Next.js)         Better Auth            Backend (FastAPI)      Database
 |                           |                         |                        |                   |
 |-- Fill Registration ----->|                         |                        |                   |
 |    Form (email, password) |                         |                        |                   |
 |                           |                         |                        |                   |
 |-- Submit ---------------->|                         |                        |                   |
 |                           |-- Register Request ---->|                        |                   |
 |                           |   (email, password)     |                        |                   |
 |                           |                         |-- INSERT user -------->|------------------>|
 |                           |                         |   (hashed password)    |                   |
 |                           |                         |                        |<------------------|
 |                           |<-- Success -------------|                        |                   |
 |                           |                         |                        |                   |
 |<-- Redirect to Login -----|                         |                        |                   |
 |                           |                         |                        |                   |
```

**Steps**:
1. User fills registration form (email, password)
2. Frontend calls Better Auth registration API
3. Better Auth validates email uniqueness and password strength
4. Better Auth creates user record in database (with hashed password)
5. Frontend redirects to login page

**Error Scenarios**:
- Email already exists → Better Auth returns error → Frontend displays "Email already registered"
- Invalid email format → Better Auth returns error → Frontend displays "Invalid email"
- Weak password → Better Auth returns error → Frontend displays password requirements

### 2. User Login Flow

```
User                  Frontend (Next.js)         Better Auth            Backend (FastAPI)      Database
 |                           |                         |                        |                   |
 |-- Fill Login Form ------->|                         |                        |                   |
 |    (email, password)      |                         |                        |                   |
 |                           |                         |                        |                   |
 |-- Submit ---------------->|                         |                        |                   |
 |                           |-- Login Request ------->|                        |                   |
 |                           |   (email, password)     |                        |                   |
 |                           |                         |-- SELECT user -------->|------------------>|
 |                           |                         |   WHERE email = ?      |                   |
 |                           |                         |                        |<------------------|
 |                           |                         |-- Verify password      |                   |
 |                           |                         |   (hash comparison)    |                   |
 |                           |                         |                        |                   |
 |                           |<-- JWT Token -----------|                        |                   |
 |                           |   {sub: user_id, ...}   |                        |                   |
 |                           |                         |                        |                   |
 |-- Store Token ----------->|                         |                        |                   |
 |   (httpOnly cookie)       |                        |                        |                   |
 |                           |                         |                        |                   |
 |<-- Redirect to Dashboard--|                         |                        |                   |
 |                           |                         |                        |                   |
```

**Steps**:
1. User fills login form (email, password)
2. Frontend calls Better Auth login API
3. Better Auth queries database for user by email
4. Better Auth verifies password (compares hash)
5. Better Auth generates JWT token with user_id in `sub` claim
6. Frontend stores JWT token securely (httpOnly cookie recommended)
7. Frontend redirects to dashboard

**Error Scenarios**:
- Email not found → Better Auth returns error → Frontend displays "Invalid credentials"
- Password incorrect → Better Auth returns error → Frontend displays "Invalid credentials"
- Account locked/disabled → Better Auth returns error → Frontend displays appropriate message

### 3. Authenticated API Request Flow

```
User              Frontend (Next.js)         Backend (FastAPI)           Database
 |                       |                           |                        |
 |-- Click "View Tasks"->|                           |                        |
 |                       |                           |                        |
 |                       |-- GET /api/{user_id}/ --->|                        |
 |                       |   tasks                   |                        |
 |                       |   Authorization: Bearer   |                        |
 |                       |   <JWT>                   |                        |
 |                       |                           |                        |
 |                       |                           |-- Extract JWT ------   |
 |                       |                           |   from header          |
 |                       |                           |                        |
 |                       |                           |-- Verify Signature -   |
 |                       |                           |   (BETTER_AUTH_SECRET) |
 |                       |                           |                        |
 |                       |                           |-- Check Expiration -   |
 |                       |                           |   (exp claim)          |
 |                       |                           |                        |
 |                       |                           |-- Extract user_id --   |
 |                       |                           |   (sub claim)          |
 |                       |                           |                        |
 |                       |                           |-- Verify URL --------   |
 |                       |                           |   user_id == sub       |
 |                       |                           |                        |
 |                       |                           |-- SELECT * FROM ------>|
 |                       |                           |   tasks WHERE          |
 |                       |                           |   user_id = ?          |
 |                       |                           |                        |
 |                       |                           |<-- Tasks --------------|
 |                       |                           |                        |
 |                       |<-- JSON Response ---------|                        |
 |                       |   {tasks: [...]}          |                        |
 |                       |                           |                        |
 |<-- Render Task List --|                           |                        |
 |                       |                           |                        |
```

**Steps**:
1. User triggers action requiring API call (e.g., view tasks)
2. Frontend retrieves JWT token from storage
3. Frontend makes API request with Authorization header: `Bearer <JWT>`
4. Backend extracts JWT from Authorization header
5. Backend verifies JWT signature using `BETTER_AUTH_SECRET`
6. Backend checks token expiration (`exp` claim vs current time)
7. Backend extracts user_id from `sub` claim
8. Backend verifies URL `{user_id}` parameter matches token `sub` claim
9. Backend queries database, filtering by authenticated user_id
10. Backend returns filtered data
11. Frontend renders response

**Security Checks** (in order):
1. Authorization header present? → If NO: **401 Unauthorized**
2. JWT format valid? → If NO: **401 Unauthorized**
3. JWT signature valid? → If NO: **401 Unauthorized**
4. JWT expired? → If NO: **401 Unauthorized**
5. URL user_id matches JWT user_id? → If NO: **403 Forbidden**
6. Task belongs to authenticated user? → If NO: **404 Not Found** (or **403 Forbidden**)

### 4. Token Expiration & Refresh Flow

```
User              Frontend (Next.js)         Backend (FastAPI)           Better Auth
 |                       |                           |                        |
 |-- API Request ------->|                           |                        |
 |                       |-- GET /api/{user_id}/ --->|                        |
 |                       |   tasks                   |                        |
 |                       |   Authorization: Bearer   |                        |
 |                       |   <EXPIRED_JWT>           |                        |
 |                       |                           |                        |
 |                       |                           |-- Verify JWT -------   |
 |                       |                           |   (expired)            |
 |                       |                           |                        |
 |                       |<-- 401 Unauthorized ------|                        |
 |                       |   {detail: "Token expired"}                        |
 |                       |                           |                        |
 |                       |-- Refresh Token ----------------------->|          |
 |                       |   Request                                |          |
 |                       |                           |              |          |
 |                       |<-- New JWT ---------------------------- |          |
 |                       |                           |              |          |
 |-- Store New Token --->|                           |              |          |
 |                       |                           |              |          |
 |                       |-- Retry API Request ----->|              |          |
 |                       |   Authorization: Bearer   |              |          |
 |                       |   <NEW_JWT>               |              |          |
 |                       |                           |              |          |
 |                       |<-- Success Response ------|              |          |
 |<-- Render Data -------|                           |              |          |
 |                       |                           |              |          |
```

**Steps**:
1. Frontend makes API request with expired token
2. Backend detects expiration and returns 401 Unauthorized
3. Frontend detects 401 and triggers refresh flow
4. Frontend calls Better Auth refresh endpoint
5. Better Auth issues new JWT token
6. Frontend stores new token
7. Frontend retries original API request with new token
8. Request succeeds

**Alternative**: Use refresh tokens (separate long-lived token for obtaining new JWTs)

## Backend JWT Verification Implementation

### Pseudocode (Python FastAPI)

```python
import jwt
from datetime import datetime
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

# Security scheme
bearer_scheme = HTTPBearer()


def verify_jwt(token: str) -> dict:
    """
    Verify JWT signature and expiration.
    Returns decoded payload if valid.
    Raises HTTPException if invalid.
    """
    try:
        # Decode and verify signature
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM]
        )

        # Check expiration (jwt.decode does this automatically)
        # But explicit check for clarity:
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature"
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> str:
    """
    Extract and return authenticated user_id from JWT.
    Dependency for protected routes.
    """
    token = credentials.credentials
    payload = verify_jwt(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user_id"
        )

    return user_id


def verify_user_id_match(url_user_id: str, token_user_id: str):
    """
    Verify that URL user_id parameter matches JWT user_id.
    Raises 403 Forbidden if mismatch.
    """
    if url_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: user_id mismatch"
        )


# Example usage in route
@app.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    auth_user_id: str = Depends(get_current_user_id)
):
    # Verify URL user_id matches authenticated user_id
    verify_user_id_match(user_id, auth_user_id)

    # Proceed with user-scoped query
    tasks = await task_service.list_tasks(auth_user_id)
    return {"tasks": tasks}
```

## Frontend JWT Storage

### Recommended: httpOnly Cookies

**Advantages**:
- Not accessible via JavaScript (XSS protection)
- Automatically included in requests
- Secure flag prevents transmission over HTTP

**Configuration** (Better Auth):
```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 7 * 24 * 60 * 60, // 7 days
  },
});
```

### Alternative: localStorage (less secure)

**Disadvantages**:
- Vulnerable to XSS attacks
- Must manually attach to requests

**Only use if**:
- httpOnly cookies are not feasible
- Additional XSS protections are in place

## Security Considerations

### 1. Shared Secret Protection
- `BETTER_AUTH_SECRET` must be strong (minimum 32 characters, random)
- Never commit secret to version control
- Use `.env` files with `.gitignore`
- Rotate secret if compromised (invalidates all existing tokens)

### 2. Token Expiration
- Short expiration (1-24 hours) reduces risk if token stolen
- Balance security vs user convenience (frequent re-logins)
- Implement refresh tokens for better UX

### 3. HTTPS in Production
- Always use HTTPS in production (prevents token interception)
- Secure cookie flag should be `true` in production

### 4. CORS Configuration
- Whitelist specific origins (not `*`)
- Development: `http://localhost:3000`
- Production: `https://yourdomain.com`

### 5. User ID Verification
- **ALWAYS** verify URL user_id matches JWT user_id
- Never trust client-provided user_id without JWT verification
- Filter ALL database queries by authenticated user_id

### 6. Error Messages
- Don't leak information in error messages
- Use generic "Invalid credentials" instead of "Email not found" or "Wrong password"
- Log detailed errors server-side for debugging

## Environment Variables

### Frontend (.env.local)

```bash
# Better Auth configuration
BETTER_AUTH_SECRET=your-secret-here-min-32-chars-random

# API endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```bash
# Better Auth secret (MUST MATCH FRONTEND)
BETTER_AUTH_SECRET=your-secret-here-min-32-chars-random

# Database connection
DATABASE_URL=postgresql://user:password@host:5432/database

# CORS allowed origins
CORS_ORIGINS=http://localhost:3000
```

**CRITICAL**: `BETTER_AUTH_SECRET` must be identical in both frontend and backend.

## Testing Authentication

### Manual Testing Steps

1. **Register User**
   - Navigate to http://localhost:3000/register
   - Enter email and password
   - Verify redirect to login

2. **Login**
   - Navigate to http://localhost:3000/login
   - Enter credentials
   - Verify redirect to dashboard
   - Open browser DevTools → Application → Cookies
   - Verify JWT cookie exists

3. **Authenticated Request**
   - On dashboard, trigger task list load
   - Open DevTools → Network tab
   - Verify Authorization header: `Bearer <token>`
   - Verify 200 OK response

4. **Invalid Token Test**
   - Modify cookie to invalid value
   - Refresh dashboard
   - Verify redirect to login (or 401 error)

5. **User ID Mismatch Test**
   - While logged in as User A, manually navigate to `/api/user-b-id/tasks`
   - Verify 403 Forbidden response

### Automated Testing (pytest example)

```python
def test_list_tasks_valid_token(client, mock_jwt):
    """Test that valid JWT allows access to tasks"""
    token = create_test_jwt(user_id="test-user-123")
    response = client.get(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_list_tasks_no_token(client):
    """Test that missing token returns 401"""
    response = client.get("/api/test-user-123/tasks")
    assert response.status_code == 401


def test_list_tasks_user_id_mismatch(client, mock_jwt):
    """Test that user_id mismatch returns 403"""
    token = create_test_jwt(user_id="user-a")
    response = client.get(
        "/api/user-b/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
```

## Future Enhancements (Phase III+)

- **Refresh Tokens**: Separate long-lived tokens for obtaining new access tokens
- **OAuth2/Social Login**: Google, GitHub authentication
- **Multi-Factor Authentication (MFA)**: TOTP, SMS codes
- **Role-Based Access Control (RBAC)**: Admin, user, viewer roles
- **API Key Authentication**: For AI agent/service-to-service access
- **Rate Limiting**: Prevent brute force attacks
- **Account Lockout**: After N failed login attempts
- **Email Verification**: Require email confirmation before account activation
- **Password Reset**: Forgot password flow with email token
