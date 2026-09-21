<<<<<<< HEAD
import importlib
import sys
from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient


PACKAGE_DIR = Path(__file__).parents[1] / "src" / "nigeria_network_detector"


@pytest.fixture
def client(monkeypatch):
	monkeypatch.syspath_prepend(str(PACKAGE_DIR))
	monkeypatch.chdir(PACKAGE_DIR)
	app_module = importlib.import_module("app")
	app_module = importlib.reload(app_module)
	return TestClient(app_module.app)


def test_detect_endpoint_returns_network_and_cleaned_number(client):
	response = client.post("/api/detect", json={"phone_number": "+234 803 123 4567"})

	assert response.status_code == 200
	assert response.json() == {
		"success": True,
		"phone_number": "+234 803 123 4567",
		"network": "MTN",
		"cleaned_number": "08031234567",
		"error": None,
	}


def test_detect_endpoint_rejects_missing_phone_number(client):
	response = client.post("/api/detect", json={"phone_number": ""})

	assert response.status_code == 200
	assert response.json() == {
		"success": False,
		"phone_number": None,
		"network": None,
		"cleaned_number": None,
		"error": "Phone number is required",
	}


def test_detect_endpoint_rejects_invalid_number(client):
	response = client.post("/api/detect", json={"phone_number": "12345"})

	assert response.status_code == 200
	assert response.json()["success"] is False
	assert response.json()["error"] == (
		"Invalid Nigerian number format: Number must be 11 digits"
	)


def test_networks_endpoint_returns_provider_metadata(client):
	response = client.get("/api/networks")

	assert response.status_code == 200
	payload = response.json()
	assert payload["success"] is True
	assert set(payload["networks"]) == {
		"MTN",
		"Glo",
		"Airtel",
		"9mobile",
		"Ntel",
		"Smile",
	}
=======
"""Integration tests for the FastAPI HTTP layer (routes, static files, app factory)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from nigeria_network_detector.app import app, create_app


class TestAppFactory:
    def test_create_app_returns_configured_instance(self):
        instance = create_app()
        assert instance.title == "Nigerian Network Detector"

    def test_module_level_app_is_usable(self):
        assert app.title == "Nigerian Network Detector"


class TestIndexPage:
    def test_root_returns_html(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Nigerian Network Detector" in response.text

    def test_static_css_is_served(self, client: TestClient):
        response = client.get("/static/css/style.css")
        assert response.status_code == 200

    def test_static_js_is_served(self, client: TestClient):
        response = client.get("/static/js/script.js")
        assert response.status_code == 200


class TestDetectEndpoint:
    def test_valid_number_returns_network(self, client: TestClient):
        response = client.post("/api/detect", json={"phone_number": "0803 123 4567"})
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["network"] == "MTN"
        assert data["cleaned_number"] == "08031234567"
        assert data["phone_number"] == "0803 123 4567"
        assert data["error"] is None

    def test_international_format(self, client: TestClient):
        response = client.post(
            "/api/detect", json={"phone_number": "+2348051234567"}
        )
        data = response.json()
        assert data["success"] is True
        assert data["network"] == "Glo"

    def test_whitespace_only_number_is_rejected(self, client: TestClient):
        response = client.post("/api/detect", json={"phone_number": "   "})
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Phone number is required"

    def test_invalid_format_is_rejected(self, client: TestClient):
        response = client.post("/api/detect", json={"phone_number": "12345"})
        data = response.json()
        assert data["success"] is False
        assert data["error"].startswith("Invalid Nigerian number format")

    def test_unknown_prefix(self, client: TestClient):
        response = client.post("/api/detect", json={"phone_number": "07001234567"})
        data = response.json()
        assert data["success"] is True
        assert data["network"] == "Unknown network"

    def test_missing_field_returns_422(self, client: TestClient):
        response = client.post("/api/detect", json={})
        assert response.status_code == 422


class TestNetworksEndpoint:
    def test_lists_all_networks(self, client: TestClient):
        response = client.get("/api/networks")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert set(data["networks"]) == {
            "MTN", "Glo", "Airtel", "9mobile", "Ntel", "Smile",
        }

    def test_each_network_has_expected_shape(self, client: TestClient):
        data = client.get("/api/networks").json()
        for info in data["networks"].values():
            assert "prefixes" in info
            assert "color" in info
            assert "description" in info
>>>>>>> a4caf25f5d7ce7f90ef5fbe4bbb9a8501ce2669b
