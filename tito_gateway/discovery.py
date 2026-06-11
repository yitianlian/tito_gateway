"""Backend URL discovery for wrapping an OpenAI-compatible server."""

from __future__ import annotations

import os
from collections.abc import Iterable, Mapping


DEFAULT_BACKEND_ENV_VARS = ("TITO_BACKEND_URL", "OPENAI_BASE_URL", "SGLANG_BASE_URL")


def normalize_backend_url(url: str) -> str:
    normalized = url.strip().rstrip("/")
    if not normalized:
        raise ValueError("backend URL is empty")
    if "://" not in normalized:
        normalized = f"http://{normalized}"
    return normalized


def discover_backend_url(
    explicit_url: str | None = None,
    *,
    env: Mapping[str, str] | None = None,
    env_vars: Iterable[str] = DEFAULT_BACKEND_ENV_VARS,
) -> str:
    """Resolve the backend URL with deterministic precedence.

    Explicit config wins, followed by environment variables in
    ``DEFAULT_BACKEND_ENV_VARS`` order. Runtime port probing belongs in a later
    round with integration tests so ambiguous local servers are not guessed.
    """
    if explicit_url:
        return normalize_backend_url(explicit_url)

    source = os.environ if env is None else env
    for key in env_vars:
        value = source.get(key)
        if value:
            return normalize_backend_url(value)

    names = ", ".join(env_vars)
    raise RuntimeError(f"backend URL not found; pass --backend-url or set one of: {names}")
