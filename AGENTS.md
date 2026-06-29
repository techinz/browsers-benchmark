# browsers-benchmark Agent Rules

Global baseline: `~/work/agent-context/AGENTS.MD`.

Repo delta:

- This repo benchmarks browser automation engines against public protection/fingerprinting targets. Treat live benchmark runs as external network activity.
- Default verification is offline only: Python syntax checks and checked-in result JSON parsing.
- Do not run live benchmark scripts, browser launches, proxy tests, CAPTCHA/reCAPTCHA checks, or external target probes unless the operator explicitly asks.
- Do not add proxy credentials, account tokens, session data, or target-specific secrets to docs, examples, logs, or config files.
- Use `bash scripts/verify.sh ci` for routine repo health checks.
