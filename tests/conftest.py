import os

# Set test environment variables BEFORE importing any app modules
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-tests-only-do-not-use-in-prod")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.api.dependencies import get_db  # noqa: E402
from app.infrastructure.database.connection import Base  # noqa: E402
from app.main import app  # noqa: E402

# Use SQLite in memory for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def registered_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "secret123",
            "name": "Test User",
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "auth@example.com",
            "password": "secret123",
            "name": "Auth User",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "auth@example.com", "password": "secret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
