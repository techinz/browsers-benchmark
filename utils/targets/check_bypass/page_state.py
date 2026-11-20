import asyncio
import json
import logging
from typing import Optional

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def wait_for_bypass(
        engine: BrowserEngine,
        success_selector: str,
        block_selector: Optional[str] = None,
        timeout_s: float = 30,
        interval_s: float = 2.5,
        min_wait_s: float = 0
) -> bool:
    """
    Poll the page until the real content is shown (success_selector present and block_selector absent)

    Polling (instead of a single check) lets challenges that resolve on their own (e.g. Cloudflare) finish,
    and requiring a positive marker means a blank/error page is never counted as a bypass.
    Uses document.querySelector via JS, so it behaves the same in every engine and returns immediately.

    :param engine: BrowserEngine instance
    :param success_selector: CSS selector that only exists on the real (unblocked) page
    :param block_selector: CSS selector that only exists on the block/captcha page
    :param timeout_s: Maximum time to wait for the real page
    :param interval_s: Time between checks
    :param min_wait_s: Wait this long before the first check (for protections that show a captcha
        on top of an already loaded page, e.g. PerimeterX)
    """

    await asyncio.sleep(min_wait_s)

    script = (
        f"const ok = !!document.querySelector({json.dumps(success_selector)});\n"
        f"const blocked = {f'!!document.querySelector({json.dumps(block_selector)})' if block_selector else 'false'};\n"
        "return JSON.stringify({ok: ok, blocked: blocked});"
    )

    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout_s
    while True:
        try:
            state = await engine.execute_js(script)
            state = json.loads(state) if isinstance(state, str) else (state or {})
            if state.get("ok") and not state.get("blocked"):
                return True
        except Exception as e:
            logger.debug(f"{engine.name}: page state check failed: {e}")

        if loop.time() >= deadline:
            return False
        await asyncio.sleep(interval_s)
