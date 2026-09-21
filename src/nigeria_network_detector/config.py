"""Application-wide configuration and constants.

Centralising these values means the FastAPI app, the CLI entry point and
the test suite can all agree on where templates/static files live and
what the app is called, without hard-coding relative paths that break
depending on the current working directory.
"""

from __future__ import annotations

from pathlib import Path

# --- App metadata -----------------------------------------------------
APP_NAME = "Nigerian Network Detector"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "Detects the mobile network operator (MTN, Glo, Airtel, 9mobile, "
    "Ntel or Smile) behind a Nigerian phone number."
)

# --- Filesystem layout --------------------------------------------------
# BASE_DIR points at the `nigeria_network_detector` package directory,
# regardless of which directory the app happens to be launched from.
BASE_DIR: Path = Path(__file__).resolve().parent
STATIC_DIR: Path = BASE_DIR / "static"
TEMPLATES_DIR: Path = BASE_DIR / "templates"

# --- Server defaults ------------------------------------------------------
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
