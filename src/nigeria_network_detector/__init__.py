"""Nigerian Network Detector.

Detects the mobile network operator (MTN, Glo, Airtel, 9mobile, Ntel or
Smile) behind a Nigerian phone number, served as a small FastAPI app.
"""

from .app import create_app
from .detector import detect_nigerian_network, get_network_prefixes

__version__ = "1.0.0"
__all__ = ["create_app", "detect_nigerian_network", "get_network_prefixes"]
