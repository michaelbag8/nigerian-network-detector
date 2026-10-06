"""Nigerian Network Detector."""

from .detector import detect_network, normalize_phone_number

__all__ = [
    "detect_network",
    "normalize_phone_number",
]

__version__ = "0.1.0"
