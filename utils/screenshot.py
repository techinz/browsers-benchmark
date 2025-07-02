import logging
import os

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def take_screenshot(engine: BrowserEngine, screenshots_path: str, target_name: str) -> None:
    """Take a screenshot for a target"""

    try:
        screenshot_path = os.path.join(screenshots_path, f"{target_name}.png")
        await engine.screenshot(screenshot_path)
    except Exception as e:
        logger.warning(f'{engine.name} failed to take screenshot for {target_name}: {e}')
