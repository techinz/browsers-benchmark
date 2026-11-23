from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, detection, page_text, wait_for

RESULT_SCRIPT = """
const raw = ((document.querySelector('#bdJsonOutput') || {}).textContent || '').trim();
try {
    const data = JSON.parse(raw);
    return JSON.stringify(data && data.verdict && data.verdict.score !== undefined ? data : null);
} catch (e) {
    return JSON.stringify(null);
}
"""


async def check_apivoid(engine: BrowserEngine) -> dict:
    """
    APIVoid Bot Detection Test - risk score 0-100 with a level (ok/warn/fail); also weighs the IP reputation.
    Obvious bots get a 403 instead of the test page, which counts as detected

    :param engine: BrowserEngine instance
    """

    result = await wait_for(engine, RESULT_SCRIPT, timeout_s=60)
    if not result:
        if "403 Forbidden" in await page_text(engine):
            return detection(BOT, "blocked (403)", risk=100, blocked=True)
        raise Exception("APIVoid result not found")

    summary = result["verdict"]
    level = summary.get("level")
    verdict = HUMAN if level == "ok" else SUSPICIOUS if level == "warn" else BOT

    return detection(
        verdict, f"risk {summary.get('score')}", risk=summary.get("score"),
        score=summary.get("score"), label=summary.get("label"), level=level,
        tampered=summary.get("tampered"), triggered_rules=summary.get("ruleCount"),
        groups={g.get("label"): g.get("status") for g in result.get("groups", [])}
    )
