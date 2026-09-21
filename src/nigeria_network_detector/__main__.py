"""Console-script entry point (used when the package is pip-installed).

Equivalent to the root-level ``main.py``, but doesn't need the ``src/``
sys.path shim since an installed package is already importable.
"""

from __future__ import annotations

import uvicorn

from .config import DEFAULT_HOST, DEFAULT_PORT


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
