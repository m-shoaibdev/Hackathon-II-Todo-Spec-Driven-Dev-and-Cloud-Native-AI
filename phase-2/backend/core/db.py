"""Database connection and session management for Neon PostgreSQL."""

from typing import Generator
from sqlmodel import Session, SQLModel, create_engine
from .config import settings


# Create database engine
# For Neon PostgreSQL, we need to enable SSL for secure connections
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # Log SQL queries in dev
    connect_args={
        "sslmode": "require",  # Neon requires SSL
    },
)


def create_db_tables() -> None:
    """Create all database tables.

    This should be called on application startup.
    Note: In production, use proper database migrations (Alembic).
    For Phase II, we'll create tables on startup for simplicity.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a database session.

    Yields:
        Session: SQLModel database session

    Usage in route:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session
