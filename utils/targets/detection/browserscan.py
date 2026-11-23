import asyncio
import re

from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, detection, grab, page_text, wait_for_text


async def check_browserscan(engine: BrowserEngine) -> dict:
    """
    BrowserScan Bot Detection - overall result ("Normal" or "Robot") plus a status per check

    :param engine: BrowserEngine instance
    """

    await wait_for_text(engine, r"Test Results:\s*\S+.*\n(Normal|Robot|Abnormal|Unknown)\n", timeout_s=60)
    await asyncio.sleep(8)  # checks keep resolving after the overall result appears
    text = await page_text(engine)

    overall = grab(text, r"Test Results:\s*([^\n]+)")
    if not overall:
        raise Exception("BrowserScan result not found")

    checks = [(name.strip(), status) for name, status in
              re.findall(r"\n([^\n]{2,60})\n(Normal|Robot|Abnormal|Unknown)(?=\n|$)", text)
              if not name.startswith("Test Results")]
    abnormal = [name for name, status in checks if status in ("Robot", "Abnormal")]
    unknown = [name for name, status in checks if status == "Unknown"]

    if abnormal or overall != "Normal":
        verdict, summary = BOT, f"{overall.lower()}, {', '.join(abnormal)}" if abnormal else overall.lower()
    elif unknown:
        verdict, summary = SUSPICIOUS, f"{len(unknown)} unknown"
    else:
        verdict, summary = HUMAN, f"{len(checks)}/{len(checks)} normal"

    return detection(verdict, summary, overall=overall, abnormal=abnormal, unknown=unknown, checks=len(checks))
