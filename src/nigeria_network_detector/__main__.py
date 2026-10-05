"""Console-script entry point. After `pip install -e .`, run with:

    nigeria-network-detector

Or directly:

    python -m nigeria_network_detector
"""

from __future__ import annotations

import os

import uvicorn

from .app import create_app


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    reload = os.environ.get("RELOAD", "true").lower() == "true"

    if reload:
        # Reload mode needs an import string, not an app instance, so
        # uvicorn can re-import the module after a file change.
        uvicorn.run("nigeria_network_detector.app:app", host=host, port=port, reload=True)
    else:
        uvicorn.run(create_app(), host=host, port=port)


if __name__ == "__main__":
    main()
