"""Entry point — run with `python main.py` to start the dev server.

Works whether or not the package has been installed (`pip install -e .`):
falls back to adding src/ to sys.path so the app can be run with zero setup
beyond `pip install fastapi uvicorn jinja2 pydantic`.
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from nigeria_network_detector.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
