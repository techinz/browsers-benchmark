import asyncio
import logging
import os

from engines.base import BrowserEngine
from utils.real_ip import mask_real_ip_js

logger = logging.getLogger(__name__)


async def take_screenshot(engine: BrowserEngine, screenshots_path: str, target_name: str) -> None:
    """
    Take a screenshot for a target

    :param engine: BrowserEngine instance
    :param screenshots_path: Path to save the screenshot
    :param target_name: Name of the target for which the screenshot is taken
    """

    # hide the real IP on the page (e.g. shown by block pages, ipify or WebRTC leaks) before capturing it
    mask_script = mask_real_ip_js()
    if mask_script:
        try:
            await asyncio.wait_for(engine.execute_js(mask_script), 15)
        except Exception as e:
            logger.warning(f'{engine.name} failed to mask the real IP before screenshot for {target_name}: {e}')

    try:
        screenshot_path = os.path.join(screenshots_path, f"{target_name}.png")
        await asyncio.wait_for(engine.screenshot(screenshot_path), 60)
    except Exception as e:
        logger.warning(f'{engine.name} failed to take screenshot for {target_name}: {e}')
