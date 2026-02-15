"""Authentication routes for user registration and login.

These routes handle:
- POST /auth/register: Create new user account
- POST /auth/login: Authenticate user and issue JWT token
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel, EmailStr, Field

from core.db import get_session
from services.auth_service import (
    register_user,
    login_user,
    DuplicateEmailError,
    InvalidCredentialsError,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Request/Response Models

class RegisterRequest(BaseModel):
    """User registration request payload."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User password (min 8 characters)"
    )
    name: str | None = Field(None, max_length=100, description="User display name")


class LoginRequest(BaseModel):
    """User login request payload."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    """Authentication response with user info and JWT token."""

    user: dict = Field(..., description="User information")
    token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


# Routes

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email and password. Returns user info and JWT token.",
)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """Register a new user account.

    Args:
        request: Registration request with email, password, and optional name
        session: Database session

    Returns:
        AuthResponse: User info and JWT access token

    Raises:
        HTTPException 400: If email is already registered
        HTTPException 422: If validation fails
    """
    try:
        # Register user
        user = register_user(
            session=session,
            email=request.email,
            password=request.password,
            name=request.name,
        )

        # Generate JWT token (registration auto-logs in)
        from services.auth_service import create_access_token
        token = create_access_token(user.id, user.email)

        return AuthResponse(
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "createdAt": user.created_at.isoformat(),
            },
            token=token,
        )

    except DuplicateEmailError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user with email and password. Returns user info and JWT token.",
)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """Login existing user.

    Args:
        request: Login request with email and password
        session: Database session

    Returns:
        AuthResponse: User info and JWT access token

    Raises:
        HTTPException 401: If credentials are invalid
        HTTPException 422: If validation fails
    """
    try:
        # Authenticate user
        user, token = login_user(
            session=session,
            email=request.email,
            password=request.password,
        )

        return AuthResponse(
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "createdAt": user.created_at.isoformat(),
            },
            token=token,
        )

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
