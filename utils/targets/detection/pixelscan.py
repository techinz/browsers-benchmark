import asyncio

from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, click, detection, evaluate, wait_for

STATE_SCRIPT = """
const state = (document.querySelector('.checker-header') || {getAttribute: () => null}).getAttribute('state');
return JSON.stringify(['success', 'error'].includes(state) ? state : null);
"""

CHECKS_SCRIPT = """
const read = (rowSelector, nameSelector, statusSelector) => [...document.querySelectorAll(rowSelector)]
    .map(row => ({
        name: ((row.querySelector(nameSelector) || {}).textContent || '').trim(),
        status: ((row.querySelector(statusSelector) || {}).textContent || '').trim()
    }))
    .filter(check => check.name && check.status);
const details = read('.bot-check-accordion__row', '.bot-check-accordion__label', '.bot-check-accordion__status');
return JSON.stringify(details.length ? details
    : read('.summary-section__text', '.summary-section__title', '.summary-section__status'));
"""


async def check_pixelscan(engine: BrowserEngine) -> dict:
    """
    Pixelscan Bot Detection Test - "You're Definitely a Human" or "Bot Behavior Detected"

    The check starts on its own when the page loads; pressing "Start Check" during it restarts and stalls it,
    so the button is only used when no check has started

    :param engine: BrowserEngine instance
    """

    await click(engine, "button", "Accept")
    await click(engine, "button", "Got it")

    state = await wait_for(engine, STATE_SCRIPT, timeout_s=30)
    if not state:
        await click(engine, ".checker-header button", "Start Check")
        state = await wait_for(engine, STATE_SCRIPT, timeout_s=60)
    if not state:
        raise Exception("Pixelscan result not found")
    await asyncio.sleep(3)

    checks = await evaluate(engine, CHECKS_SCRIPT) or []
    not_clear = [f"{c['name']}: {c['status']}" for c in checks if c["status"] != "Clear"]

    if state == "success":
        verdict, summary = HUMAN, f"{len(checks) - len(not_clear)}/{len(checks)} clear"
    else:
        verdict, summary = BOT, f"{len(not_clear)} not clear" if not_clear else "bot behavior"

    return detection(verdict, summary, state=state, not_clear=not_clear, checks=len(checks))
