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
