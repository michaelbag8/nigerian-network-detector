#!/usr/bin/env python3
"""Entry point for the Nigerian Network Detector.

Run the app with:

    python main.py

or, once installed (`pip install -e .`), with:

    nigeria-network-detector

Either way this starts a Uvicorn server serving the FastAPI app defined
in ``src/nigeria_network_detector/app.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make `src/` importable even when the package hasn't been `pip install`-ed
# (e.g. running `python main.py` straight from a fresh checkout).
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import uvicorn  # noqa: E402

from nigeria_network_detector.config import DEFAULT_HOST, DEFAULT_PORT  # noqa: E402


def main() -> None:
    """Start the development server."""
    uvicorn.run(
        "nigeria_network_detector.app:app",
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
