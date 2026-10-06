"""Nigerian Network Detector — detects the original allocated network for a
Nigerian mobile number from its prefix.

Public surface kept intentionally small: the app factory for anyone wiring
this into a bigger deployment, and the pure detection functions for anyone
who wants network-detection without pulling in FastAPI at all.
"""

# from .app import create_app
# from .detector import detect_network, normalize_phone_number

# __all__ = ["create_app", "detect_network", "normalize_phone_number"]

# __version__ = "0.1.0"
from .detector import detect_network, normalize_phone_number

__all__ = ["detect_network", "normalize_phone_number"]

__version__ = "0.1.0"
