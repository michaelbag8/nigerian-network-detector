"""Pure phone-number normalization and network-detection logic.

Deliberately free of any FastAPI/Starlette imports: this module should be
fully unit-testable on its own, and reusable from a script, a different
web framework, or a batch job, without needing a running server.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# NOTE: this is a small demo table covering the sample ranges shown on the
# homepage. A production deployment should source this from a verified,
# NCC-backed prefix database (a `providers` + `phone_prefixes` table pair)
# rather than a hardcoded dict in source code — prefixes are periodically
# reallocated, and that data shouldn't require a code deploy to update.
_PREFIX_TABLE: dict[str, str] = {
    "0803": "mtn", "0806": "mtn", "0703": "mtn", "0706": "mtn", "0813": "mtn",
    "0816": "mtn", "0810": "mtn", "0814": "mtn", "0903": "mtn", "0906": "mtn",
    "0805": "glo", "0807": "glo", "0905": "glo", "0815": "glo", "0811": "glo",
    "0802": "airtel", "0808": "airtel", "0708": "airtel", "0812": "airtel",
    "0701": "airtel", "0902": "airtel", "0907": "airtel", "0901": "airtel",
    "0809": "9mobile", "0817": "9mobile", "0818": "9mobile", "0908": "9mobile",
    "0909": "9mobile",
}

_NATIONAL_FORMAT_RE = re.compile(r"^0\d{10}$")


@dataclass(frozen=True)
class Provider:
    """A mobile network provider, as shown in the UI."""

    slug: str
    name: str
    color: str
    text_color: str


PROVIDERS: dict[str, Provider] = {
    "mtn": Provider(slug="mtn", name="MTN Nigeria", color="#FFCB05", text_color="#1A1600"),
    "glo": Provider(slug="glo", name="Glo Mobile", color="#0C8A3E", text_color="#FFFFFF"),
    "airtel": Provider(slug="airtel", name="Airtel Nigeria", color="#E4252B", text_color="#FFFFFF"),
    "9mobile": Provider(slug="9mobile", name="9mobile Nigeria", color="#0A5C3A", text_color="#FFFFFF"),
}


@dataclass(frozen=True)
class NormalizedNumber:
    """The result of normalizing a user-typed number.

    `national` is always populated (even when invalid) so error messages
    and logs can reference what was actually parsed out of the input.
    """

    national: str  # e.g. "09050003328"
    e164: str       # e.g. "+2349050003328" — empty string when invalid
    valid: bool


def normalize_phone_number(raw: str) -> NormalizedNumber:
    """Normalize a Nigerian number typed as 0905…, +234…, 234…, with
    spaces or dashes, into one canonical national + E.164 representation.
    """
    digits = re.sub(r"[\s\-()]", "", raw or "")

    if digits.startswith("+234"):
        digits = "0" + digits[4:]
    elif digits.startswith("234") and not digits.startswith("0"):
        digits = "0" + digits[3:]

    valid = bool(_NATIONAL_FORMAT_RE.match(digits))
    e164 = f"+234{digits[1:]}" if valid else ""

    return NormalizedNumber(national=digits, e164=e164, valid=valid)


@dataclass(frozen=True)
class DetectionResult:
    """Everything the API/UI needs to describe one lookup."""

    normalized: NormalizedNumber
    prefix: str
    provider: Provider | None


def detect_network(raw: str) -> DetectionResult:
    """Normalize `raw` and look up its original/allocated network.

    This only ever answers "original network" — see the prefix table note
    above and the README for why that's not the same as "current network"
    once Mobile Number Portability is in the picture.
    """
    normalized = normalize_phone_number(raw)
    prefix = normalized.national[:4] if normalized.valid else ""
    provider_slug = _PREFIX_TABLE.get(prefix) if normalized.valid else None
    provider = PROVIDERS.get(provider_slug) if provider_slug else None

    return DetectionResult(normalized=normalized, prefix=prefix, provider=provider)
