"""
Unit tests for FastAPI temperature and version endpoints.
"""

from unittest.mock import patch
import pytest
from httpx import AsyncClient, ASGITransport
from app import app

# pylint: disable=too-few-public-methods
class MockResponse:
    """Mock response object for requests.get()."""

    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        """Return mocked JSON data."""
        return self._json_data


mock_sensors_response = {
    "sensors": [
        {"_id": "sensor123", "title": "Temperatur"},
        {"_id": "sensor999", "title": "Humidity"},
    ]
}

mock_data_response = [{"value": "21.0"}]


@pytest.mark.asyncio
async def test_version():
    """Test /version endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/version")
    assert response.status_code == 200
    assert response.json() == {"app_version": "v0.0.2"}


@pytest.mark.asyncio
@patch("app.requests.get")
async def test_temperature(mock_get):
    """Test /temperature endpoint with mocked data."""
    def mock_get_side_effect(url, **kwargs):  # Accept **kwargs here
        if "/sensors" in url:
            return MockResponse(mock_sensors_response)
        return MockResponse(mock_data_response)

    mock_get.side_effect = mock_get_side_effect

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/temperature")

    expected_avg = (21.0 + 21.0 + 21.0) / 3
    assert response.status_code == 200
    assert response.json() == {"avg_temp": str(expected_avg)}

