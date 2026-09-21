"""HTTP routes: the page route and the small JSON API the frontend calls."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import APP_NAME, TEMPLATES_DIR
from .detector import clean_phone_number, detect_nigerian_network, get_network_prefixes
from .schemas import DetectionResponse, NetworksResponse, PhoneNumberRequest

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request) -> HTMLResponse:
    """Serve the single-page app."""
    return templates.TemplateResponse(
        request, "index.html", {"app_name": APP_NAME}
    )


@router.post("/api/detect", response_model=DetectionResponse, tags=["detection"])
async def detect_network(payload: PhoneNumberRequest) -> DetectionResponse:
    """Detect the network operator for the given phone number."""
    phone_number = payload.phone_number.strip()

    if not phone_number:
        return DetectionResponse(success=False, error="Phone number is required")

    network = detect_nigerian_network(phone_number)

    if network.startswith("Invalid Nigerian number format"):
        return DetectionResponse(success=False, error=network)

    return DetectionResponse(
        success=True,
        phone_number=phone_number,
        network=network,
        cleaned_number=clean_phone_number(phone_number),
    )


@router.get("/api/networks", response_model=NetworksResponse, tags=["detection"])
async def get_networks() -> NetworksResponse:
    """List every supported network, its prefixes, brand color and description."""
    return NetworksResponse(success=True, networks=get_network_prefixes())
