"""Authentication service for user registration and login.

This service handles:
1. Password hashing with bcrypt
2. User registration with duplicate email prevention
3. User login with credential verification
4. JWT token generation for authenticated sessions
"""

from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import jwt

from models.user import User
from core.config import settings


# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthServiceError(Exception):
    """Base exception for authentication service errors."""
    pass


class DuplicateEmailError(AuthServiceError):
    """Raised when attempting to register with an existing email."""
    pass


class InvalidCredentialsError(AuthServiceError):
    """Raised when login credentials are invalid."""
    pass


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Bcrypt hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT access token for authenticated user.

    Args:
        user_id: User's unique identifier
        email: User's email address

    Returns:
        str: JWT access token

    Token payload includes:
        - sub: user_id (subject)
        - email: user's email
        - exp: expiration timestamp
        - iat: issued at timestamp
    """
    now = datetime.utcnow()
    expires = now + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    payload = {
        "sub": user_id,  # Standard JWT claim for user ID
        "email": email,
        "iat": now,
        "exp": expires,
    }

    token = jwt.encode(
        payload,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def register_user(
    session: Session,
    email: str,
    password: str,
    name: Optional[str] = None,
) -> User:
    """Register a new user with email and password.

    Args:
        session: Database session
        email: User's email address (must be unique)
        password: User's plain text password (will be hashed)
        name: Optional display name

    Returns:
        User: Newly created user object

    Raises:
        DuplicateEmailError: If email is already registered
    """
    # Check for duplicate email
    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise DuplicateEmailError(f"Email already registered: {email}")

    # Generate user ID (simple approach for Phase II)
    # In production, use UUID or let Better Auth manage this
    user_id = f"user_{email.split('@')[0]}_{datetime.utcnow().timestamp()}"

    # Hash password
    hashed_password = hash_password(password)

    # Create user with hashed password
    user = User(
        id=user_id,
        email=email,
        password_hash=hashed_password,
        name=name,
        created_at=datetime.utcnow(),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def login_user(session: Session, email: str, password: str) -> tuple[User, str]:
    """Authenticate user and generate JWT token.

    Args:
        session: Database session
        email: User's email address
        password: User's plain text password

    Returns:
        tuple[User, str]: User object and JWT access token

    Raises:
        InvalidCredentialsError: If credentials are invalid
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        raise InvalidCredentialsError("Invalid email or password")

    # CRITICAL: Verify password against stored hash
    # This ensures only correct passwords are accepted
    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Invalid email or password")

    # Generate JWT token only after successful password verification
    token = create_access_token(user.id, user.email)

    return user, token
