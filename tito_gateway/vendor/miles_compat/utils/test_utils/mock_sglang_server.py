"""Lightweight compatibility subset of Miles mock SGLang server utilities."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProcessResultMetaInfo:
    weight_version: str | None = None
    routed_experts: str | None = None
    spec_accept_token_num: int | None = None
    spec_draft_token_num: int | None = None
    spec_verify_ct: int | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass(frozen=True)
class ProcessResult:
    text: str
    finish_reason: str = "stop"
    cached_tokens: int = 0
    meta_info: ProcessResultMetaInfo = ProcessResultMetaInfo()


ProcessFn = Callable[[str], ProcessResult]
