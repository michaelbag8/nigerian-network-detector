from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from nigeria_network_detector.app import create_app


@pytest.fixture()
def client() -> TestClient:
    """A fresh TestClient per test — create_app() has no side effects,
    so there's no shared state to worry about between tests."""
    return TestClient(create_app())
