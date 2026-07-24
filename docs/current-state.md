# browsers-benchmark Current State

Updated: 2026-07-06 JST

## Purpose

`browsers-benchmark` is a Python browser automation benchmark toolkit for
comparing engines against public protection and fingerprinting targets.

## Runtime And Reproducibility

- Runtime selector: `.python-version` is `3.12`.
- Dependency file: `requirements.txt`.
- Offline verifier: `scripts/verify.sh`.
- CI workflow: `.github/workflows/verify.yml` uses `actions/checkout@v6`,
  `actions/setup-python@v6`, `.python-version`, and `bash scripts/verify.sh ci`.

## Verification Contract

- `bash scripts/verify.sh ci`: offline syntax and checked-in JSON checks.
- `bash scripts/verify.sh syntax`: compile Python files without importing browser/proxy dependencies.
- `bash scripts/verify.sh json`: parse checked-in result JSON files.

This verifier intentionally does not install browser engines, launch browsers,
use proxies, solve CAPTCHAs, or contact external protection targets.

## Safety Boundaries

- Treat live benchmark runs as external network activity.
- Do not run browser launches, proxy tests, CAPTCHA/reCAPTCHA checks, or target probes without explicit operator request.
- Do not add proxy credentials, AdsPower API keys, account tokens, session data, or target-specific secrets to docs, examples, logs, or config files.
- Keep `.env`, proxy files, browser profiles, and generated live artifacts out of public cleanup work unless separately approved and sanitized.

## Current Cleanup Status

- Repo state before this pass: clean.
- Documentation capsule added: `docs/index.md`, `docs/current-state.md`, `docs/cleanup-roadmap.md`.
- README links the docs capsule and keeps the offline verification command near setup.
- Deferred checks: live benchmark execution, browser installation, proxy validation, and E2E target probing.
