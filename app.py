# pylint: disable=import-error
"""
FastAPI app providing temperature data from OpenSenseMap API.
"""

from datetime import datetime, timedelta, timezone
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI
import requests
from starlette.responses import Response

app = FastAPI()


@app.get("/version")
async def root():
    """Return application version."""
    return {"app_version": "v0.0.2"}

@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics in text format."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/temperature")
async def temperature():
    """Return average temperature from multiple sense boxes."""
    avg_temp = 0
    count = 0
    sense_boxes_ids = [
        "5eba5fbad46fb8001b799786",
        "5c21ff8f919bf8001adf2488",
        "5ade1acf223bd80019a1011c"
    ]

    for sense_box_id in sense_boxes_ids:
        response = requests.get(
            f"https://api.opensensemap.org/boxes/{sense_box_id}/sensors",
             timeout=5
        )
        sensors = response.json().get("sensors", [])

        temper_sensor_id = next(
            (sensor["_id"] for sensor in sensors if sensor["title"] == "Temperatur"),
            None
        )

        if not temper_sensor_id:
            continue  # Skip if no temperature sensor found

        from_date = (
            datetime.now(timezone.utc) - timedelta(hours=1)
        ).isoformat().replace("+00:00", "Z")

        data_url = (
            f"https://api.opensensemap.org/boxes/{sense_box_id}/data/"
            f"{temper_sensor_id}?from-date={from_date}"
        )
        temperatures = requests.get(data_url, timeout=5).json()

        if temperatures:
            last_temperature_value = temperatures[0]["value"]
            avg_temp += float(last_temperature_value)
            count += 1  
    if count == 0:
        return {"avg_temp": "0", "status": "No Data"}

    avg_temp = avg_temp / count

    # Decide status based on avg_temp
    if avg_temp < 10:
        status = "Too Cold"
    elif 11 <= avg_temp <= 36:
        status = "Good"
    else:
        status = "Too Hot"
  
    return {"avg_temp": str(round(avg_temp, 2)), "status": status}