"""Core detection logic: no FastAPI, no I/O — pure functions over strings.

Keeping this module framework-free makes it trivial to unit test and to
reuse (CLI, batch jobs, another web framework, ...) without dragging in
FastAPI.
"""

from __future__ import annotations

import re

# Networks are checked longest-prefix-first (5 digits) then 4 digits, so
# more specific prefixes such as MTN's 07025/07026 win over the more
# general 4-digit prefixes of the same leading digits.
NETWORK_PREFIXES: dict[str, dict[str, object]] = {
    "MTN": {
        "prefixes": [
            "0803", "0806", "0703", "0706", "0813", "0816", "0810", "0814",
            "0903", "0906", "0913", "0916", "0704", "07025", "07026",
        ],
        "color": "#ffcd00",
        "description": "Largest network in Nigeria",
    },
    "Glo": {
        "prefixes": ["0805", "0807", "0705", "0815", "0811", "0905", "0915"],
        "color": "#228b22",
        "description": "Affordable data provider",
    },
    "Airtel": {
        "prefixes": [
            "0802", "0808", "0708", "0701", "0812", "0902", "0901",
            "0904", "0907", "0912",
        ],
        "color": "#e91e63",
        "description": "Quality network provider",
    },
    "9mobile": {
        "prefixes": ["0809", "0818", "0817", "0909", "0908"],
        "color": "#0066cc",
        "description": "Former Etisalat network",
    },
    "Ntel": {
        "prefixes": ["0804"],
        "color": "#9c27b0",
        "description": "4G LTE provider",
    },
    "Smile": {
        "prefixes": ["0702"],
        "color": "#ff9800",
        "description": "4G broadband services",
    },
}


def clean_phone_number(phone_number: str) -> str:
    """Strip formatting and normalise a Nigerian number to local 0XXXXXXXXXX form.

    Accepts local (0803 123 4567), international (+234 803 123 4567 /
    234803...) and bare 10-digit (803 123 4567) input, in each case
    returning the 11-digit local form starting with ``0``.
    """
    cleaned = re.sub(r"\D", "", str(phone_number))

    if cleaned.startswith("234") and len(cleaned) > 10:
        # International format, e.g. "2348031234567" -> "08031234567".
        cleaned = "0" + cleaned[3:]
    elif len(cleaned) == 10 and not cleaned.startswith("0"):
        # Bare form with the leading 0 omitted, e.g. "8031234567".
        cleaned = "0" + cleaned

    return cleaned


def validate_nigerian_number(cleaned_number: str) -> tuple[bool, str]:
    """Validate an already-cleaned number is a well-formed Nigerian mobile number."""
    if not cleaned_number.isdigit():
        return False, "Number must contain only digits"

    if len(cleaned_number) != 11:
        return False, "Number must be 11 digits"

    if not cleaned_number.startswith("0"):
        return False, "Number must start with 0"

    return True, "Valid"


def get_network_prefixes() -> dict[str, dict[str, object]]:
    """Return all network prefixes and metadata, organised by provider."""
    return NETWORK_PREFIXES


def detect_nigerian_network(phone_number: str) -> str:
    """Detect the network provider of a Nigerian phone number.

    Args:
        phone_number: The phone number to check, in any supported format.

    Returns:
        The network provider name, ``"Unknown network"`` if the number is
        well-formed but its prefix isn't recognised, or a message starting
        with ``"Invalid Nigerian number format"`` if the number is malformed.
    """
    cleaned_number = clean_phone_number(phone_number)

    is_valid, message = validate_nigerian_number(cleaned_number)
    if not is_valid:
        return f"Invalid Nigerian number format: {message}"

    networks = get_network_prefixes()

    five_digit_prefix = cleaned_number[:5]
    for network, info in networks.items():
        if five_digit_prefix in info["prefixes"]:
            return network

    four_digit_prefix = cleaned_number[:4]
    for network, info in networks.items():
        if four_digit_prefix in info["prefixes"]:
            return network

    return "Unknown network"
