# TITO Gateway

TITO Gateway is a standalone Python package and CLI wrapper around the Miles
Agentic Chat Template / TITO session-server work. The TITO tokenizer, fixed
chat-template approach, session trajectory model, proxy behavior, and verifier
flow come from Miles and its contributors.

This repository is a packaging and usage layer for that work. It does not
rewrite the Miles TITO algorithms. The vendored source audit is recorded in
`tito_gateway/VENDORED_MILES_AUDIT.md`, and copied upstream tests are kept as a
compatibility contract.

## Acknowledgement

This package explicitly credits Miles as the source of the underlying TITO
implementation being wrapped here:

- Miles repository: https://github.com/radixark/miles
- Miles documentation: https://www.radixark.com/miles/docs/user-guide/agentic-chat-template

When vendoring Miles source, preserve upstream notices and keep the audit file
updated.

## Python Usage

Use `TITOGateway` beside an existing OpenAI-compatible backend. The gateway
serves Miles session routes and proxies chat completions to the backend while
maintaining TITO session/token state.

```python
from tito_gateway import TITOGateway, TITOGatewayConfig

gateway = TITOGateway(
    TITOGatewayConfig(
        hf_checkpoint="Qwen/Qwen3-0.6B",
        backend_url="http://127.0.0.1:8000",
        chat_template_path=None,
        apply_chat_template_kwargs={"enable_thinking": False},
        tito_model="qwen3",
        tito_allowed_append_roles=("tool", "user"),
        session_server_ip="127.0.0.1",
        session_server_port=30000,
    )
)

app = gateway.app
```

`hf_checkpoint` is required. Constructing the gateway without it fails before
startup instead of silently enabling broken TITO tracking.

## CLI Usage

After installing the package, `tito-gateway` starts the gateway. The default
command is `serve`, so these forms are equivalent:

```bash
tito-gateway --hf-checkpoint Qwen/Qwen3-0.6B \
  --tito-model qwen3 \
  --tito-allowed-append-roles tool user \
  --backend-url http://127.0.0.1:8000 \
  --session-server-port 30000
```

```bash
tito-gateway serve --hf-checkpoint Qwen/Qwen3-0.6B \
  --tito-model qwen3 \
  --tito-allowed-append-roles tool user \
  --backend-url http://127.0.0.1:8000 \
  --session-server-port 30000
```

Template kwargs use JSON, matching the Miles convention:

```bash
tito-gateway serve --hf-checkpoint Qwen/Qwen3-0.6B \
  --backend-url http://127.0.0.1:8000 \
  --apply-chat-template-kwargs '{"enable_thinking": false}'
```

In an editable checkout where the console script is not installed into `PATH`,
the same parser can be exercised with:

```bash
python -m tito_gateway.cli serve --help
```

## Backend Discovery

Backend selection is deterministic and fail-closed:

1. Explicit `backend_url` / `--backend-url`.
2. Environment variables in this order:
   - `TITO_BACKEND_URL`
   - `OPENAI_BASE_URL`
   - `SGLANG_BASE_URL`
3. Configured probe candidates, in order.

Probe candidates are checked with bounded timeouts. For each candidate, the
gateway probes `/health` first and `/v1/models` second. The first live
candidate wins and the selected source is logged. If no explicit URL, env var,
or live probe candidate exists, startup raises a clear error instead of binding
a gateway that cannot proxy calls.

CLI probe candidates are repeatable:

```bash
tito-gateway serve --hf-checkpoint Qwen/Qwen3-0.6B \
  --backend-probe-candidate http://127.0.0.1:8000 \
  --backend-probe-candidate http://127.0.0.1:30000 \
  --backend-probe-timeout 0.5
```

## Verification Commands

`verify-chat-template` delegates to the migrated Miles chat-template verifier:

```bash
tito-gateway verify-chat-template --template path/to/template.jinja --thinking off
```

`verify-session-tito-tokenizer` preserves a Miles-style verifier parser surface
and runs the migrated Miles/SGLang session verifier when the optional training
stack is installed:

```bash
tito-gateway verify-session-tito-tokenizer \
  --hf-checkpoint Qwen/Qwen3-4B \
  --tito-model qwen3 \
  --tito-allowed-append-roles tool user \
  --sglang-reasoning-parser qwen3 \
  --sglang-tool-call-parser qwen25 \
  --rollout-num-gpus-per-engine 1
```

In a CPU-fast environment without the optional Miles/SGLang training stack, the
command exits with a clear dependency/runtime error. That dependency-gated exit
must not be treated as a GPU/e2e verification pass.

## Test Setup

The copied upstream fast tests use tokenizer assets from Hugging Face. Prepare
the local tokenizer cache without downloading model weights:

```bash
python scripts/prepare_test_tokenizer_cache.py --endpoint https://huggingface.co
```

Run the CPU-fast verification suite:

```bash
pytest tests/upstream tests/package -q
```

Useful targeted checks:

```bash
pytest tests/upstream/fast/utils/chat_template_utils/test_tito_tokenizer.py
pytest tests/upstream/fast/utils/chat_template_utils/test_pretokenized_via_tito.py
pytest tests/upstream/fast/router/test_sessions.py
pytest tests/upstream/fast/router/test_session_race_conditions.py
pytest tests/upstream/fast/router/test_session_pretokenized_e2e.py
pytest tests/upstream/fast/utils/test_utils/test_session_verify_runner.py
pytest tests/package
```

CLI smoke checks:

```bash
tito-gateway --help
tito-gateway serve --help
tito-gateway verify-chat-template --help
tito-gateway verify-session-tito-tokenizer --help
```
