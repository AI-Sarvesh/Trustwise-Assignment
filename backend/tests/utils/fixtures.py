import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal

@pytest.fixture
def test_client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def test_db():
    """Fixture for test database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_texts():
    """Fixture for test text samples"""
    return [
        "This is a short test text",
        "This is a longer test text with more words to analyze" * 10,
        "Complex text with emotions: I am happy but also worried",
        "Technical text about programming and algorithms"
    ] 