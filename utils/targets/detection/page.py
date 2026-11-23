import asyncio
import json
import re
from typing import Any, Optional

from engines.base import BrowserEngine

HUMAN = "human"
SUSPICIOUS = "suspicious"
BOT = "bot"

VERDICT_RISK = {HUMAN: 0, SUSPICIOUS: 50, BOT: 100}


def detection(verdict: str, summary: str, risk: Optional[float] = None, **details: Any) -> dict:
    """
    Build the result of a bot detection test

    :param verdict: HUMAN, SUSPICIOUS or BOT - how the site classified the browser
    :param summary: Short, human-readable result shown in the report (e.g. "risk 41")
    :param risk: 0 (human) - 100 (bot) on the site's own numeric scale; sites without one use the verdict
    :param details: Site-specific data kept in the raw results
    """

    return {
        "verdict": verdict,
        "summary": summary,
        "risk": round(risk) if risk is not None else VERDICT_RISK[verdict],
        "details": details,
    }


async def evaluate(engine: BrowserEngine, script: str) -> Any:
    """
    Run a script that returns JSON.stringify(...) and decode its result

    :param engine: BrowserEngine instance
    :param script: JavaScript function body
    """

    raw = await engine.execute_js(script)
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None
    return raw


async def page_text(engine: BrowserEngine) -> str:
    """
    Get the visible text of the page

    :param engine: BrowserEngine instance
    """

    text = await engine.execute_js("return document.body ? document.body.innerText : '';")
    return text if isinstance(text, str) else ""


async def wait_for(engine: BrowserEngine, script: str, timeout_s: float = 45, interval_s: float = 1) -> Any:
    """
    Poll a script until it returns a truthy value

    :param engine: BrowserEngine instance
    :param script: JavaScript function body that returns JSON.stringify(...)
    :param timeout_s: Maximum time to wait
    :param interval_s: Time between checks
    :return: The last value returned by the script (falsy on timeout)
    """

    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout_s
    value = None
    while True:
        try:
            value = await evaluate(engine, script)
        except Exception:
            value = None
        if value or loop.time() >= deadline:
            return value
        await asyncio.sleep(interval_s)


async def wait_for_text(engine: BrowserEngine, pattern: str, timeout_s: float = 45, interval_s: float = 1) -> str:
    """
    Poll the page text until it matches a regex

    :param engine: BrowserEngine instance
    :param pattern: Regex to search for in the visible text
    :param timeout_s: Maximum time to wait
    :param interval_s: Time between checks
    :return: The page text (whether or not it matched)
    """

    regex = re.compile(pattern, re.S)
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout_s
    while True:
        try:
            text = await page_text(engine)
        except Exception:
            text = ""
        if regex.search(text) or loop.time() >= deadline:
            return text
        await asyncio.sleep(interval_s)


async def click(engine: BrowserEngine, selector: str, text: Optional[str] = None) -> bool:
    """
    Click the first visible element matching a selector (and containing a text)

    :param engine: BrowserEngine instance
    :param selector: CSS selector
    :param text: Text the element must contain
    :return: Whether an element was clicked
    """

    script = (
        f"const el = [...document.querySelectorAll({json.dumps(selector)})]"
        f".find(e => e.offsetParent !== null && (!{json.dumps(text)} || e.textContent.includes({json.dumps(text)})));\n"
        "if (el) el.click();\n"
        "return JSON.stringify(!!el);"
    )
    try:
        return bool(await evaluate(engine, script))
    except Exception:
        return False


def grab(text: str, pattern: str) -> Optional[str]:
    """
    Get the first group of a regex match

    :param text: Text to search
    :param pattern: Regex with one group
    """

    match = re.search(pattern, text, re.S)
    return match.group(1).strip() if match else None
