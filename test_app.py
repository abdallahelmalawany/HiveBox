# pylint: disable=import-error
import pytest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from app import app  # ✅ import your FastAPI app from app.py


# Mocked responses
mock_sensors_response = {
    "sensors": [
        {"_id": "sensor123", "title": "Temperatur"},
        {"_id": "sensor999", "title": "Humidity"},
    ]
}

mock_data_response = [{"value": "21.0"}]


class MockResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


@pytest.mark.asyncio
async def test_version():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/version")
    assert response.status_code == 200
    assert response.json() == {"app_version": "v0.0.2"}


@pytest.mark.asyncio
@patch("app.requests.get")  # ✅ patch requests.get in app.py
async def test_temperature(mock_get):
    def mock_get_side_effect(url, *args, **kwargs):
        if "/sensors" in url:
            return MockResponse(mock_sensors_response)
        elif "/data/" in url:
            return MockResponse(mock_data_response)

    mock_get.side_effect = mock_get_side_effect

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/temperature")

    assert response.status_code == 200
    expected_avg = (21.0 + 21.0 + 21.0) / 3
    assert response.json() == {"avg_temp": str(expected_avg)}

