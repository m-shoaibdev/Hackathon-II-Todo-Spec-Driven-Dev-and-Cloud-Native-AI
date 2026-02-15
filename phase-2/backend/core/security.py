"""JWT token verification for Better Auth tokens.

This module provides utilities for verifying JWT tokens issued by Better Auth
on the frontend. The backend validates tokens using the shared secret but does
not issue tokens (Better Auth handles that).
"""

from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status

from .config import settings


class JWTVerificationError(Exception):
    """Custom exception for JWT verification failures."""
    pass


def verify_jwt_token(token: str) -> dict:
    """Verify a JWT token and extract the payload.

    Args:
        token: JWT token string (without 'Bearer' prefix)

    Returns:
        dict: Decoded JWT payload containing user claims

    Raises:
        JWTVerificationError: If token is invalid, expired, or malformed

    Example payload:
        {
            "sub": "user_123abc",  # User ID
            "email": "user@example.com",
            "exp": 1234567890,     # Expiration timestamp
            "iat": 1234567800      # Issued at timestamp
        }
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )

        # Validate required claims
        user_id: Optional[str] = payload.get("sub")
        if not user_id:
            raise JWTVerificationError("Token missing 'sub' claim (user_id)")

        return payload

    except JWTError as e:
        raise JWTVerificationError(f"Invalid token: {str(e)}")


def get_user_id_from_token(token: str) -> str:
    """Extract user_id from JWT token.

    Args:
        token: JWT token string (without 'Bearer' prefix)

    Returns:
        str: User ID from token 'sub' claim

    Raises:
        HTTPException: 401 Unauthorized if token is invalid
    """
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: missing user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except JWTVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_user_id_match(token_user_id: str, url_user_id: str) -> None:
    """Validate that the user_id from JWT matches the URL parameter.

    This is a critical security check to prevent users from accessing
    other users' resources by manipulating URL parameters.

    Args:
        token_user_id: User ID extracted from JWT token
        url_user_id: User ID from URL path parameter

    Raises:
        HTTPException: 403 Forbidden if user_ids don't match
    """
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: user_id mismatch - cannot access other users' resources",
        )
