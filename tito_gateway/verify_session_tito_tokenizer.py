"""Dependency-gated entrypoint for Miles session-server TITO e2e verification."""

from __future__ import annotations

from typing import Any


def run_from_args(args: Any) -> int:
    """Run the optional session TITO verifier when the e2e runner is available.

    The real Miles verifier boots rollout/SGLang infrastructure and needs the
    broader training/e2e stack. This package exposes the compatible argument
    surface now, while failing clearly when that runner has not been vendored.
    """
    try:
        from miles.utils.test_utils.session_verify_runner import run_session_verify
    except Exception as exc:
        print(
            "verify-session-tito-tokenizer requires the optional Miles/SGLang "
            "session e2e runner, which is not installed in this package yet.",
        )
        print(f"Missing runner detail: {type(exc).__name__}: {exc}")
        return 2

    run_session_verify(args=args)
    return 0
