import json

from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, detection, wait_for_text


def _parse_report(text: str) -> dict | None:
    start = text.find("{", max(text.find('"isBot"') - 20, 0))
    if start < 0:
        return None
    depth = 0
    for end, char in enumerate(text[start:], start):
        depth += {"{": 1, "}": -1}.get(char, 0)
        if depth == 0:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                return None
    return None


async def check_deviceandbrowserinfo(engine: BrowserEngine) -> dict:
    """
    DeviceAndBrowserInfo "Are you a bot?" - isBot plus the individual detection signals

    The report sometimes stays empty on the first load, so the page is reloaded once before giving up

    :param engine: BrowserEngine instance
    """

    report = _parse_report(await wait_for_text(engine, r'"isBot"\s*:\s*(true|false)', timeout_s=30))
    if not report:
        await engine.reload_page()
        report = _parse_report(await wait_for_text(engine, r'"isBot"\s*:\s*(true|false)', timeout_s=30))
    if not report:
        raise Exception("DeviceAndBrowserInfo result not found")

    signals = [name for name, value in (report.get("details") or {}).items() if value]

    signals_text = f"{len(signals)} signal{'' if len(signals) == 1 else 's'}"
    if report.get("isBot"):
        verdict, summary = BOT, f"bot, {signals_text}"
    elif signals:
        verdict, summary = SUSPICIOUS, signals_text
    else:
        verdict, summary = HUMAN, "human"

    return detection(verdict, summary, is_bot=report.get("isBot"), signals=signals)
