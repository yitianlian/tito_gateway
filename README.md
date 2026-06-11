# TITO Gateway

TITO Gateway is a standalone packaging and wrapper effort around the Miles TITO
session-server work. The TITO tokenizer, fixed chat-template strategy, session
trajectory model, proxy behavior, and verification approach are credited to the
Miles project and its contributors.

This package exists to make that work easier to import beside an existing
OpenAI-compatible server or launch from a small CLI. It is not a rewrite of the
Miles TITO algorithms; the implementation is structured so upstream Miles logic
can be vendored and tested with minimal edits.

## Current Scope

- Importable `tito_gateway` package.
- `TITOGatewayConfig` and `TITOGateway` wrapper shell.
- Deterministic backend URL discovery from explicit config and environment.
- `tito-gateway` CLI with Miles-compatible serve flags.
- Vendored Miles TITO/chat-template/session core under `tito_gateway.vendor.miles_compat`.
- A `miles` compatibility namespace for upstream-style imports used by Miles tests.

Unchanged upstream test migration and full e2e verifier wiring are tracked in
`plan.md` and subsequent RLCR rounds.

## Acknowledgement

This project acknowledges Miles as the source of the underlying TITO design and
implementation being packaged here:

- Repository: https://github.com/radixark/miles
- Documentation: https://www.radixark.com/miles/docs/user-guide/agentic-chat-template

Any vendored Miles source should preserve upstream notices and be recorded in
`tito_gateway/upstream.json`.
