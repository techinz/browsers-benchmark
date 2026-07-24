# Cleanup Roadmap

Updated: 2026-07-06 JST

## Current Status

- Repo state before this pass: clean.
- Public entrypoint: `README.md`.
- Runtime selector: `.python-version` (`3.12`).
- Offline verifier: `scripts/verify.sh`.
- Live benchmark runs: gated external network activity.

## Verified This Pass

- `bash scripts/verify.sh ci`: offline syntax and checked-in JSON checks.
- `git diff --check`: whitespace check.

## Roadmap

1. Keep README as the public entrance.
   - Preserve overview, feature list, sample result context, installation, offline verification, and disclaimer.
   - Keep long operational status in `docs/current-state.md` instead of growing README.
2. Keep `docs/current-state.md` as the live boundary snapshot.
   - Update runtime, CI, offline verifier, and live-run restrictions when contracts change.
   - Explicitly list deferred live checks instead of implying they were run.
3. Keep `docs/index.md` as the documentation map.
   - Link new runbooks there before adding more top-level README links.
4. Keep `scripts/verify.sh` offline by default.
   - It may parse checked-in result JSON and compile Python.
   - It must not install browsers, launch browsers, use proxies, or contact external targets without a separate explicit target and approval.
5. Treat proxy and provider changes as higher-risk.
   - Never add real proxy credentials, AdsPower keys, account tokens, cookies, or session files to docs or examples.
   - Live benchmark artifacts should be reviewed for sensitive IP/account/session data before publication.

## Open Items

- Add a sanitized live-run checklist if the operator asks to run real benchmarks.
- Add official/source evidence before changing GitHub Actions versions, browser install behavior, proxy handling, or external target assumptions.
- Consider a short `docs/results-publication.md` before publishing new benchmark artifacts.
