"""Database configuration and session management."""
from sqlmodel import Session, create_engine
from .config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


def get_db():
    """
    Dependency to get database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
