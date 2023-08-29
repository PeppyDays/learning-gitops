import pytest
from fastapi.testclient import TestClient

from order.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
