import asyncio

from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, detection, grab, page_text, wait_for_text


def _percent(text: str, label: str) -> int | None:
    value = grab(text, rf"(\d+)% {label}:")
    return int(value) if value is not None else None


async def check_creepjs(engine: BrowserEngine) -> dict:
    """
    CreepJS headless/stealth analysis - any "headless" or "stealth" percentage above 0 means detected

    "like headless" is reported but not used for the verdict, regular desktop browsers score around 30-50% there

    :param engine: BrowserEngine instance
    """

    await wait_for_text(engine, r"\d+% stealth:", timeout_s=60)
    await asyncio.sleep(5)
    text = await page_text(engine)

    like_headless, headless, stealth = (_percent(text, label) for label in ("like headless", "headless", "stealth"))
    if headless is None or stealth is None:
        raise Exception("CreepJS headless/stealth result not found")

    verdict = BOT if headless or stealth else HUMAN
    return detection(
        verdict, f"headless {headless}%, stealth {stealth}%", risk=max(headless, stealth),
        like_headless=like_headless, headless=headless, stealth=stealth
    )
