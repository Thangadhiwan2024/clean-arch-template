"""Entrypoint for the server"""

import uvicorn
from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title="Vizor For Data",
    version="1.0.0",
)


@app.get("/")
async def status() -> dict:
    """Health check endpoint.

    Returns:
        dict: A dictionary with the status of the service.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
    )
