# Round 0 Contract

## One Mainline Objective

Create the initial installable `tito_gateway` package scaffold with explicit Miles acknowledgement, a minimal importable wrapper API, deterministic backend URL discovery, and a CLI shell that preserves the key Miles-compatible serve flags.

## Target ACs

- AC-1: Package import surface works.
- AC-4: CLI starts gateway with Miles-compatible arguments.

AC-5 is partially touched only where backend discovery is needed by the wrapper API, but full runtime probing is not a Round 0 completion requirement.

## Blocking Side Issues In Scope

None known at round start.

## Queued Side Issues Out Of Scope

- Full upstream Miles TITO/session vendoring and unchanged upstream test migration.
- Real FastAPI session proxy runtime parity with Miles.
- Optional GPU/e2e `verify-session-tito-tokenizer` support.

## Round Success Criteria

- `pyproject.toml` defines an installable package and `tito-gateway` console script.
- `tito_gateway` imports and exports `TITOGateway`, `TITOGatewayConfig`, `SessionServer`, and `get_tito_tokenizer`.
- README/package metadata clearly acknowledge Miles and position this as a wrapper/packaging effort around Miles TITO work.
- CLI help and core serve argument parsing work without importing heavy optional Miles/SGLang training dependencies.
- Focused Round 0 tests pass for import surface, config validation, backend discovery precedence, and CLI help.
