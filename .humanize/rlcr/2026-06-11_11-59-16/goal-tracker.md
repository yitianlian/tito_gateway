# Goal Tracker

<!--
This file tracks the ultimate goal, acceptance criteria, and plan evolution.
It prevents goal drift by maintaining a persistent anchor across all rounds.

RULES:
- IMMUTABLE SECTION: Do not modify after initialization
- MUTABLE SECTION: Update each round, but document all changes
- Every task must be in one of: Active, Completed, or Deferred
- Deferred items require explicit justification
-->

## IMMUTABLE SECTION
<!-- Do not modify after initialization -->

### Ultimate Goal

把 Miles 文档中 Agentic Chat Template / TITO session-server 路径抽成一个独立 Python package。这个项目必须明确 ack Miles 同学/团队的原创工作，定位为“对 Miles TITO 工作的封装、复用和使用层”，不是重新发明或改写 Miles 的算法。核心算法尽可能原样复用 Miles upstream 代码，不重写、不改测试逻辑。新 package 需要同时支持两种使用方式：

1. Python import 方式：应用在已有 server 旁边包裹一层 gateway，自动发现或接收后端 OpenAI-compatible server 地址，捕捉 `/v1/chat/completions` 调用并维护 TITO session/token 轨迹。
2. CLI 方式：一行命令启动 gateway，参数与 Miles 对应 TITO/session-server 参数保持兼容，尤其是 `--hf-checkpoint`、`--chat-template-path`、`--apply-chat-template-kwargs`、`--tito-model`、`--tito-allowed-append-roles`、`--session-server-ip`、`--session-server-port`、router/backend URL 相关参数。

## Source Exploration Summary

### Acceptance Criteria
<!-- Each criterion must be independently verifiable -->
<!-- Claude must extract or define these in Round 0 -->


- AC-1: Package import surface works.
  - Positive Tests (expected to PASS):
    - `python -c "import tito_gateway; from tito_gateway import TITOGateway, SessionServer, get_tito_tokenizer"` succeeds.
    - A test constructs `TITOGateway(...)` with an explicit backend URL and starts the same FastAPI route behavior as Miles `SessionServer`.
  - Negative Tests (expected to FAIL):
    - Constructing gateway without `hf_checkpoint` raises the same skip/error behavior defined by the wrapper contract, without silently enabling broken TITO tracking.

- AC-2: Miles TITO core logic is reused with minimal source edits.
  - Positive Tests (expected to PASS):
    - Upstream copied tests for `TITOTokenizer`, fixed-template resolution, decode-roundtrip verifier, and session routes pass without test body edits.
    - A source audit shows `tito_tokenizer.py`, fixed templates, `template.py`, `token_seq_comparator.py`, `linear_trajectory.py`, `sessions.py`, and session error/type models are copied verbatim except import path rewrites required by package namespace.
  - Negative Tests (expected to FAIL):
    - Any implementation that rewrites TITO merge/tokenize algorithms instead of vendoring upstream code fails review.

- AC-3: Existing Miles tests are preserved.
  - Positive Tests (expected to PASS):
    - Migrated tests keep assertions, parametrization, expected failures, and mock trajectory behavior identical to upstream.
    - Compatibility shims make original import paths usable where practical, e.g. `miles.utils.chat_template_utils...` can resolve to vendored modules during tests.
  - Negative Tests (expected to FAIL):
    - Changing upstream test assertions, deleting negative tests like buggy Qwen3 boundary tests, or weakening expected mismatch checks is not allowed.

- AC-4: CLI starts gateway with Miles-compatible arguments.
  - Positive Tests (expected to PASS):
    - `tito-gateway --hf-checkpoint Qwen/Qwen3-0.6B --tito-model qwen3 --tito-allowed-append-roles tool user --backend-url http://127.0.0.1:8000 --session-server-port 30000` starts the FastAPI gateway.

---

## MUTABLE SECTION
<!-- Update each round with justification for changes -->

### Plan Version: 1 (Updated: Round 0)

#### Plan Evolution Log
<!-- Document any changes to the plan with justification -->
| Round | Change | Reason | Impact on AC |
|-------|--------|--------|--------------|
| 0 | Initial plan | - | - |

#### Active Tasks
<!-- Mainline tasks only: each task must directly advance the current round objective and carry routing metadata -->
| Task | Target AC | Status | Tag | Owner | Notes |
|------|-----------|--------|-----|-------|-------|
| [mainline] Scaffold package metadata and attribution | AC-1, AC-2 | completed | coding | claude | Verified by package tests and README/upstream metadata review |
| [mainline] Add importable wrapper API and backend discovery | AC-1, AC-5 | completed | coding | claude | Verified by package tests and import smoke |
| [mainline] Add CLI shell with Miles-compatible serve flags | AC-4 | completed | coding | claude | Verified by CLI help smoke |
| [mainline] Add focused package tests for Round 0 surface | AC-1, AC-4, AC-5 | completed | coding | claude | `pytest tests/package` passed: 11 tests |

### Blocking Side Issues
<!-- Only issues that directly block current mainline progress belong here -->
| Issue | Discovered Round | Blocking AC | Resolution Path |
|-------|-----------------|-------------|-----------------|

### Queued Side Issues
<!-- Non-blocking issues stay queued and must NOT replace the round objective -->
| Issue | Discovered Round | Why Not Blocking | Revisit Trigger |
|-------|-----------------|------------------|-----------------|
| Full upstream Miles TITO/session vendoring and unchanged upstream test migration | 0 | Round 0 is scoped to package scaffold/import/CLI foundation only | Start next round targeting AC-2/AC-3/AC-6 |
| Optional GPU/e2e `verify-session-tito-tokenizer` implementation | 0 | Requires broader Miles/SGLang dependency strategy beyond Round 0 | After core vendored session gateway passes CPU-fast tests |

### Completed and Verified
<!-- Only move tasks here after Codex verification -->
| AC | Task | Completed Round | Verified Round | Evidence |
|----|------|-----------------|----------------|----------|
| AC-1 | Package metadata/import surface/API shell | 0 | 0 | `pytest tests/package` passed; `python -c "import tito_gateway; from tito_gateway import TITOGateway, SessionServer, get_tito_tokenizer"` printed `ok` |
| AC-4 | CLI shell with Miles-compatible serve flags | 0 | 0 | `python -m tito_gateway.cli --help` and `python -m tito_gateway.cli serve --help` exited 0 and showed expected flags |
| AC-5 | Deterministic explicit/env backend discovery foundation | 0 | 0 | `tests/package/test_config_discovery.py` covered explicit precedence, env precedence, missing backend failure, JSON kwargs, invalid roles |

### Explicitly Deferred
<!-- Items here require strong justification -->
| Task | Original AC | Deferred Since | Justification | When to Reconsider |
|------|-------------|----------------|---------------|-------------------|
