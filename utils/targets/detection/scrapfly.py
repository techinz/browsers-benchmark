import asyncio

from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, click, detection, wait_for

RESULT_SCRIPT = """
const items = [...document.querySelectorAll('.detection-item-header')].map(item => ({
    name: ((item.querySelector('.detection-item-name') || {}).textContent || '').trim(),
    status: ((item.querySelector('.tool-status') || {}).textContent || '').trim().toUpperCase()
}));
if (!items.length || items.some(i => !i.status)) return JSON.stringify(null);
return JSON.stringify({
    label: ((document.querySelector('#verdict-text') || {}).textContent || '').trim(),
    items: items
});
"""


async def check_scrapfly(engine: BrowserEngine) -> dict:
    """
    Scrapfly Automation Detector - every signal is SAFE, SUSPICIOUS or DETECTED

    :param engine: BrowserEngine instance
    """

    await click(engine, "button", "Maybe later")

    if not await wait_for(engine, RESULT_SCRIPT, timeout_s=45):
        raise Exception("Scrapfly result not found")
    await asyncio.sleep(3)
    result = await wait_for(engine, RESULT_SCRIPT, timeout_s=10)

    detected = [i["name"] for i in result["items"] if i["status"] == "DETECTED"]
    suspicious = [i["name"] for i in result["items"] if i["status"] == "SUSPICIOUS"]

    if detected:
        verdict, summary = BOT, f"{len(detected)} detected"
    elif suspicious:
        verdict, summary = SUSPICIOUS, f"{len(suspicious)} suspicious"
    else:
        verdict, summary = HUMAN, f"{len(result['items'])}/{len(result['items'])} safe"

    return detection(
        verdict, summary,
        label=result["label"], detected=detected, suspicious=suspicious, total=len(result["items"])
    )
