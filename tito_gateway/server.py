"""Lightweight session server wrapper around the Miles session-server contract."""

from __future__ import annotations

from typing import Any


class SessionServer:
    """Defer concrete Miles session-server behavior until vendoring is complete."""

    def __init__(self, args: Any, backend_url: str):
        self.args = args
        self.backend_url = backend_url
        self.app = self._build_placeholder_app()

    def _build_placeholder_app(self):
        try:
            from fastapi import FastAPI
        except ImportError as exc:
            raise RuntimeError("fastapi is required to construct SessionServer") from exc

        app = FastAPI(title="TITO Gateway")

        @app.get("/health")
        async def health():
            return {"status": "ok", "backend_url": self.backend_url}

        return app
