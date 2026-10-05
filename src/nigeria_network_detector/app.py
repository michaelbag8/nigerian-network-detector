"""FastAPI app factory.

A factory (rather than a bare module-level `app = FastAPI()`) keeps the
app constructible in tests without import-time side effects, and keeps
main.py / __main__.py from needing to know how the app is wired.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import APP_NAME, APP_VERSION, STATIC_DIR
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION)

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    app.include_router(router)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        # Normalizes every HTTPException into the same {"error": {code,
        # message}} shape, whether it was raised with a dict detail (our
        # routes) or a plain string (FastAPI's own routing errors, e.g. a
        # 404 Not Found) — so API consumers only ever handle one shape,
        # and nothing leaks a Python traceback to the client.
        detail = exc.detail
        if isinstance(detail, dict) and "code" in detail and "message" in detail:
            body = {"error": detail}
        else:
            body = {"error": {"code": "HTTP_ERROR", "message": str(detail)}}
        return JSONResponse(status_code=exc.status_code, content=body)

    return app


# Module-level instance for `uvicorn nigeria_network_detector.app:app --reload`.
app = create_app()
