"""Pydantic models for the JSON API — kept separate from routes.py so the
response shape is defined once and reflected automatically in /docs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class NetworkInfo(BaseModel):
    """A provider as returned in an API response."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str
    name: str
    color: str
    text_color: str = Field(alias="textColor")


class PhoneCheckResponse(BaseModel):
    """Response body for GET /api/v1/phone/{phone_number}."""

    phone_number: str
    country: str = "NG"
    valid: bool
    prefix: str
    original_network: NetworkInfo | None
    # Always null in this build: no real-time MNP/carrier lookup is wired
    # in, so we never claim to know the *current* network — only the one
    # the prefix was originally allocated to.
    current_network: NetworkInfo | None = None
    ported: bool | None = None
    detection_type: str


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
