"""Shared pytest fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from nigeria_network_detector.app import app


@pytest.fixture()
def client() -> TestClient:
    """A TestClient wired to the app, for integration/route tests."""
    return TestClient(app)
