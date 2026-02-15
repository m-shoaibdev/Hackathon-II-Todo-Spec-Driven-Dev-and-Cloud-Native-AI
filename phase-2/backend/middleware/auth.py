"""Authentication middleware for JWT validation.

This module provides FastAPI dependencies for protecting routes
and extracting authenticated user information from JWT tokens.
"""

from typing import Annotated
from fastapi import Depends, Header, HTTPException, status

from core.security import get_user_id_from_token


def get_token_from_header(authorization: str = Header(...)) -> str:
    """Extract JWT token from Authorization header.

    Args:
        authorization: Authorization header value (e.g., "Bearer <token>")

    Returns:
        str: JWT token without 'Bearer' prefix

    Raises:
        HTTPException: 401 if header is missing or malformed
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check for "Bearer " prefix
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return parts[1]  # Return token without "Bearer" prefix


async def get_current_user_id(
    token: Annotated[str, Depends(get_token_from_header)]
) -> str:
    """FastAPI dependency to get authenticated user ID from JWT token.

    This dependency:
    1. Extracts JWT token from Authorization header
    2. Verifies token signature and expiration
    3. Extracts user_id from token payload

    Usage in routes:
        @app.get("/api/{user_id}/tasks")
        async def get_tasks(
            user_id: str,
            current_user_id: str = Depends(get_current_user_id)
        ):
            # Verify user_id matches JWT
            if user_id != current_user_id:
                raise HTTPException(status_code=403, detail="Forbidden")

            # Fetch tasks for current_user_id
            ...

    Args:
        token: JWT token extracted from Authorization header

    Returns:
        str: Authenticated user's ID

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing claims
    """
    # get_user_id_from_token handles all validation and raises appropriate HTTPExceptions
    return get_user_id_from_token(token)


# Type alias for cleaner route signatures
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
