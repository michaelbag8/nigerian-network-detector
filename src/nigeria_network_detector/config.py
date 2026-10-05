"""App metadata and resolved paths.

Centralizing these means templates/, static/, and the FastAPI app's
title/version are each defined once, not duplicated across modules.
"""

from __future__ import annotations

from pathlib import Path

APP_NAME = "Nigerian Network Detector"
APP_VERSION = "0.1.0"

PACKAGE_DIR = Path(__file__).resolve().parent
STATIC_DIR = PACKAGE_DIR / "static"
TEMPLATES_DIR = PACKAGE_DIR / "templates"
