"""Public tokenizer entrypoints reserved for Miles TITO vendoring."""

from __future__ import annotations

from enum import Enum
from typing import Any


class TITOTokenizerType(str, Enum):
    DEFAULT = "default"
    QWEN3 = "qwen3"
    QWEN35 = "qwen35"
    QWENNEXT = "qwennext"
    GLM47 = "glm47"
    NEMOTRON3 = "nemotron3"
    KIMI25 = "kimi25"
    KIMI26 = "kimi26"
    MINIMAX_M25 = "minimax_m25"
    MINIMAX_M27 = "minimax_m27"
    DEEPSEEKV32 = "deepseekv32"
    DEEPSEEKV4 = "deepseekv4"


def get_tito_tokenizer(*args: Any, **kwargs: Any) -> Any:
    """Return the vendored Miles TITO tokenizer.

    The import surface is intentionally present in Round 0. The implementation
    is completed when the Miles tokenizer code is vendored unchanged in the
    AC-2/AC-3 round.
    """
    raise NotImplementedError(
        "Miles TITO tokenizer vendoring is not installed yet; see plan.md AC-2/AC-3."
    )
