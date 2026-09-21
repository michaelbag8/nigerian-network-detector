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

<<<<<<< HEAD
@app.post("/api/detect", response_model=DetectionResponse)
async def detect_network(request: PhoneNumberRequest):
    try:
        phone_number = request.phone_number
        
        if not phone_number:
            return DetectionResponse(
                success=False,
                error="Phone number is required"
            )
        
        result = detect_nigerian_network(phone_number)
        
        if result.startswith("Invalid Nigerian number format"):
            return DetectionResponse(
                success=False,
                error=result
            )
        
        # Extract cleaned number from the detection function
        from detector import clean_phone_number
        cleaned_number = clean_phone_number(phone_number)
        
        return DetectionResponse(
            success=True,
            phone_number=phone_number,
            network=result,
            cleaned_number=cleaned_number
        )
    
    except Exception as e:
        return DetectionResponse(
            success=False,
            error=str(e)
        )
=======
>>>>>>> a4caf25f5d7ce7f90ef5fbe4bbb9a8501ce2669b

# Module-level instance so `uvicorn nigeria_network_detector.app:app` and
# `from nigeria_network_detector.app import app` both work.
app = create_app()
