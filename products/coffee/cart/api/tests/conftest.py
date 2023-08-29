import pytest
from fastapi.testclient import TestClient

from cart.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
