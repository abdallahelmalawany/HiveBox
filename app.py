# pylint: disable=import-error
"""This module sets up a FastAPI application with basic endpoints."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Fetch the current average temperature from openSenseMap API."""
    return {"Hello": "World"}
