# browsers-benchmark Docs

This repository benchmarks browser automation engines against public protection
and fingerprinting targets. Live benchmark runs are external network activity.

## Primary Sources

- [README.md](../README.md): user-facing overview, setup, sample results, and architecture.
- [AGENTS.md](../AGENTS.md): repo-local safety rules and offline verification policy.
- [scripts/verify.sh](../scripts/verify.sh): offline verifier for syntax and checked-in JSON parsing.
- [.python-version](../.python-version): local and CI Python selector.
- [.github/workflows/verify.yml](../.github/workflows/verify.yml): GitHub Actions offline verification workflow.

## Operational Notes

- [current-state.md](current-state.md): current runtime, CI, verification, and live-run boundaries.
- [cleanup-roadmap.md](cleanup-roadmap.md): README/docs/verifier cleanup plan and future update queue.

## Local Verification

Routine verification is offline:

```bash
bash scripts/verify.sh ci
```

Targeted checks:

```bash
bash scripts/verify.sh syntax
bash scripts/verify.sh json
git diff --check
```

Do not run live benchmark scripts, browser launches, proxy tests, CAPTCHA or
reCAPTCHA checks, or external target probes unless explicitly requested.
