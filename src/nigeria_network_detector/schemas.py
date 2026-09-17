"""Pydantic request/response models shared across the API routes."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PhoneNumberRequest(BaseModel):
    """Body of a POST /api/detect request."""

    phone_number: str = Field(
        ...,
        min_length=1,
        description="A Nigerian phone number in local (0803...), "
        "international (+234803...) or bare (803...) format.",
        examples=["0803 123 4567"],
    )


class DetectionResponse(BaseModel):
    """Response returned by POST /api/detect."""

    success: bool
    phone_number: str | None = None
    network: str | None = None
    cleaned_number: str | None = None
    error: str | None = None


class NetworkInfo(BaseModel):
    """Metadata about a single network operator."""

    prefixes: list[str]
    color: str
    description: str


class NetworksResponse(BaseModel):
    """Response returned by GET /api/networks."""

    success: bool
    networks: dict[str, NetworkInfo] | None = None
    error: str | None = None
