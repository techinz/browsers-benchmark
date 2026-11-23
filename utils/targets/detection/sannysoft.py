import asyncio

from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, detection, evaluate, wait_for

RESULT_SCRIPT = """
const rows = [...document.querySelectorAll('td.passed, td.failed, td.warn')].map(td => ({
    test: ((td.parentElement.cells[0] || {}).innerText || '').replace(/\\s+/g, ' ').trim(),
    status: td.classList.contains('failed') ? 'failed' : td.classList.contains('warn') ? 'warn' : 'passed'
}));
return JSON.stringify(rows.length ? rows : null);
"""

IS_FIREFOX_SCRIPT = "return JSON.stringify(/Firefox\\//.test(navigator.userAgent));"


async def check_sannysoft(engine: BrowserEngine) -> dict:
    """
    Sannysoft bot test - every check is marked passed, warn or failed

    Chrome-only checks (window.chrome) fail in every real Firefox too, so they are skipped for Firefox engines

    :param engine: BrowserEngine instance
    """

    if not await wait_for(engine, RESULT_SCRIPT, timeout_s=30):
        raise Exception("Sannysoft result not found")
    await asyncio.sleep(8)  # some checks (WebGL, permissions) finish later
    rows = await wait_for(engine, RESULT_SCRIPT, timeout_s=10)

    if await evaluate(engine, IS_FIREFOX_SCRIPT):
        rows = [r for r in rows if not r["test"].startswith("Chrome")]

    failed = [r["test"] for r in rows if r["status"] == "failed"]
    warn = [r["test"] for r in rows if r["status"] == "warn"]

    if failed:
        verdict, summary = BOT, f"{len(failed)} failed"
    elif warn:
        verdict, summary = SUSPICIOUS, f"{len(warn)} warn"
    else:
        verdict, summary = HUMAN, f"{len(rows)}/{len(rows)} passed"

    return detection(verdict, summary, failed=failed, warn=warn, checks=len(rows))
