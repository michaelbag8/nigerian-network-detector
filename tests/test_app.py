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
