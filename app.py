# pylint: disable=import-error
"""
FastAPI app providing temperature data from OpenSenseMap API.
"""

from datetime import datetime, timedelta, timezone
from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/version")
async def root():
    """Return application version."""
    return {"app_version": "v0.0.2"}


@app.get("/temperature")
async def temperature():
    """Return average temperature from multiple sense boxes."""
    avg_temp = 0
    sense_boxes_ids = [
        "5eba5fbad46fb8001b799786",
        "5c21ff8f919bf8001adf2488",
        "5ade1acf223bd80019a1011c"
    ]

    for sense_box_id in sense_boxes_ids:
        response = requests.get(
            f"https://api.opensensemap.org/boxes/{sense_box_id}/sensors"
        )
        sensors = response.json()["sensors"]
        temper_sensor_id = ""

        for sensor in sensors:
            if sensor["title"] == "Temperatur":
                temper_sensor_id = sensor["_id"]

        from_date = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
        temperatures = requests.get(
            f"https://api.opensensemap.org/boxes/{sense_box_id}/data/{temper_sensor_id}?from-date={from_date}"
        ).json()

        last_temperature_value = temperatures[0]["value"]
        avg_temp += float(last_temperature_value)

    return {"avg_temp": str(avg_temp / len(sense_boxes_ids))}