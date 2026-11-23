from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, click, detection, wait_for

RESULT_SCRIPT = """
const score = (document.querySelector('#ct-bot-score') || {}).textContent || '';
const signals = [...document.querySelectorAll('#ct-bot-breakdown tr')]
    .map(tr => {
        const pill = tr.querySelector('[class^="ct-pill-"]');
        return pill ? {name: tr.cells[0].innerText.trim(), status: pill.className.replace('ct-pill-', '')} : null;
    })
    .filter(Boolean);
if (!/\\d/.test(score) || !signals.length) return JSON.stringify(null);
return JSON.stringify({
    score: parseInt(score),
    label: ((document.querySelector('#ct-bot-badge') || {}).textContent || '').trim(),
    flagged: signals.filter(s => s.status === 'flag').map(s => s.name),
    weak: signals.filter(s => s.status === 'soft').map(s => s.name),
    checked: signals.length
});
"""


async def check_cleantalk(engine: BrowserEngine) -> dict:
    """
    CleanTalk "Am I a Bot?" - Human Score 0-100 (80+ looks human, 50-79 needs review, below 50 bot)

    The test runs on its own when the page loads, "Run the Bot Test" would only start it again

    :param engine: BrowserEngine instance
    """

    await click(engine, "button", "Accept cookies")

    result = await wait_for(engine, RESULT_SCRIPT, timeout_s=45)
    if not result:
        raise Exception("CleanTalk result not found")

    score = result["score"]
    verdict = HUMAN if score >= 80 else SUSPICIOUS if score >= 50 else BOT
    return detection(
        verdict, f"score {score}",
        score=score, label=result["label"], flagged=result["flagged"], weak=result["weak"],
        signals_checked=result["checked"]
    )
