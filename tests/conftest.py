import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from amigo.main import app
from amigo.models import Base

# Use a different database for tests, for example, a SQLite in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    # Create a new session for the test
    db = TestingSessionLocal()
    yield db
    # Rollback and clean up the database
    db.rollback()
    # Drop the tables after the test is done
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client
