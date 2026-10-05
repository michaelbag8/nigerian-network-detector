from __future__ import annotations


class TestHomepage:
    def test_serves_html(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "NetCheck NG" in response.text

    def test_links_static_assets(self, client):
        response = client.get("/")
        assert "/static/css/style.css" in response.text
        assert "/static/js/script.js" in response.text


class TestHealthAndVersion:
    def test_health(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_version(self, client):
        response = client.get("/api/v1/version")
        assert response.status_code == 200
        assert "version" in response.json()


class TestPhoneCheckEndpoint:
    def test_valid_glo_number_local_format(self, client):
        response = client.get("/api/v1/phone/09050003328")
        assert response.status_code == 200

        body = response.json()
        assert body["valid"] is True
        assert body["prefix"] == "0905"
        assert body["phone_number"] == "+2349050003328"
        assert body["detection_type"] == "prefix"
        assert body["current_network"] is None
        assert body["ported"] is None
        assert body["original_network"]["slug"] == "glo"
        assert body["original_network"]["name"] == "Glo Mobile"

    def test_valid_number_plus_234_format(self, client):
        response = client.get("/api/v1/phone/%2B2349050003328")
        assert response.status_code == 200
        assert response.json()["original_network"]["slug"] == "glo"

    def test_valid_number_234_format(self, client):
        response = client.get("/api/v1/phone/2349050003328")
        assert response.status_code == 200
        assert response.json()["original_network"]["slug"] == "glo"

    def test_mtn_number(self, client):
        response = client.get("/api/v1/phone/08030000000")
        assert response.status_code == 200
        assert response.json()["original_network"]["slug"] == "mtn"

    def test_airtel_number(self, client):
        response = client.get("/api/v1/phone/08020000000")
        assert response.status_code == 200
        assert response.json()["original_network"]["slug"] == "airtel"

    def test_9mobile_number(self, client):
        response = client.get("/api/v1/phone/08100000000".replace("0810", "0809"))
        assert response.status_code == 200
        assert response.json()["original_network"]["slug"] == "9mobile"

    def test_invalid_letters_returns_422(self, client):
        response = client.get("/api/v1/phone/abc123")
        assert response.status_code == 422
        body = response.json()
        assert body["error"]["code"] == "INVALID_PHONE_NUMBER"

    def test_special_characters_returns_422(self, client):
        response = client.get("/api/v1/phone/0905$$$3328")
        assert response.status_code == 422

    def test_too_long_returns_422(self, client):
        response = client.get("/api/v1/phone/" + "0" * 40)
        assert response.status_code == 422

    def test_too_short_returns_422(self, client):
        response = client.get("/api/v1/phone/0803000")
        assert response.status_code == 422

    def test_unsupported_prefix_returns_404(self, client):
        response = client.get("/api/v1/phone/08990000000")
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "PREFIX_NOT_FOUND"

    def test_error_body_never_leaks_a_traceback(self, client):
        response = client.get("/api/v1/phone/abc123")
        body = response.json()
        assert set(body.keys()) == {"error"}
        assert set(body["error"].keys()) == {"code", "message"}
