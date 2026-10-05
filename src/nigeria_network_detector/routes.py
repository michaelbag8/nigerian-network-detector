"""HTTP routes.

Routes stay thin on purpose: they translate HTTP <-> Python, and nothing
else. All the actual detection logic lives in detector.py, which has no
idea FastAPI exists — that split is what makes detector.py trivial to
unit test and routes.py trivial to read.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import APP_VERSION, TEMPLATES_DIR
from .detector import detect_network
from .schemas import ErrorResponse, NetworkInfo, PhoneCheckResponse

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {})


@router.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/v1/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION}


@router.get(
    "/api/v1/phone/{phone_number}",
    response_model=PhoneCheckResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Prefix not in the known table"},
        422: {"model": ErrorResponse, "description": "Not a valid Nigerian mobile number"},
    },
)
def check_phone(phone_number: str) -> PhoneCheckResponse:
    if not phone_number.strip():
        raise HTTPException(
            status_code=422,
            detail={"code": "INVALID_PHONE_NUMBER", "message": "A phone number is required."},
        )

    result = detect_network(phone_number)

    if not result.normalized.valid:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "INVALID_PHONE_NUMBER",
                "message": "That doesn't look like a valid Nigerian mobile number.",
            },
        )

    if result.provider is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "PREFIX_NOT_FOUND",
                "message": f"Prefix {result.prefix} isn't in the known prefix table.",
            },
        )

    original_network = NetworkInfo(
        slug=result.provider.slug,
        name=result.provider.name,
        color=result.provider.color,
        textColor=result.provider.text_color,
    )

    return PhoneCheckResponse(
        phone_number=result.normalized.e164,
        valid=True,
        prefix=result.prefix,
        original_network=original_network,
        detection_type="prefix",
    )
