# Development Notes

[Docs Home](index.md) | [中文](development.zh-CN.md)

## Source Policy

This package is a public wrapper around Miles' work. The implementation should
reuse the upstream logic wherever possible.

Maintenance rules:

- Preserve Miles attribution and upstream notices.
- Keep the vendored source audit current.
- Prefer wrapper code over changing TITO algorithms.
- Keep copied upstream tests as the compatibility contract.
- Do not weaken negative tests.

## Public Documentation Standard

Public docs should make the relationship clear:

- Miles owns the underlying TITO design and implementation.
- This package makes that work importable and runnable as a standalone gateway.
- Optional heavy verification depends on the Miles/SGLang training stack.

## Pre-Push Checklist

1. Run CPU-fast tests.
2. Run CLI help smoke checks.
3. Confirm staged files do not include cache, model weights, credentials, or local env files.
4. Run a secret scan over staged and outgoing changes.
5. Check `git diff --check`.

## Current Secret Guard

The `guard-secret` skill can be used before pushing. If installed, run it before
`git push` and only push when it reports `SAFE_TO_PUSH`.
