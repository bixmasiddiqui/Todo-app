"""Pytest configuration and fixtures for testing."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.main import app
from src.database import get_db


@pytest.fixture(name="session")
def session_fixture():
    """Create a new database session for each test.

    Uses an in-memory SQLite database for fast, isolated testing.

    Yields:
        Session: SQLModel database session
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with overridden database dependency.

    Args:
        session: Test database session

    Yields:
        TestClient: FastAPI test client
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
