"""Vercel entrypoint.

Vercel imports the app directly from the project root, but this project keeps
its Python package under src/. Adding that directory to sys.path here makes the
installed app and the direct-root import behave the same way.
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from nigeria_network_detector.app import app  # noqa: E402
