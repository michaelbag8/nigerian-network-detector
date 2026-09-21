"""FastAPI application factory.

Kept deliberately thin: this module wires together config, static files
and the router. Business logic lives in `detector.py`, request/response
shapes live in `schemas.py`, and the HTTP surface lives in `routes.py`.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import APP_DESCRIPTION, APP_NAME, APP_VERSION, STATIC_DIR
from .routes import router


def create_app() -> FastAPI:
    """Build and return a configured FastAPI application instance."""
    app = FastAPI(
        title=APP_NAME,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
    )

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    app.include_router(router)

    return app


# Module-level instance so `uvicorn nigeria_network_detector.app:app` and
# `from nigeria_network_detector.app import app` both work.
app = create_app()
