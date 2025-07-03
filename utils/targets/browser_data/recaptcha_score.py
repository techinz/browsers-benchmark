import asyncio
import json
import logging

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def get_recaptcha_score_data(engine: BrowserEngine, tries: int = 5) -> dict:
    """Extract data from Recaptcha Score Detector page"""

    try:
        for i in range(tries):
            await asyncio.sleep(5)

            element_found, element_html = await engine.locator('pre.response')
            if element_found:
                data = json.loads(element_html)
                break
        else:
            raise Exception("Failed to extract recaptcha score data (recaptcha score not found, out of tries)")

        return data
    except Exception as e:
        raise Exception(f"Failed to extract recaptcha score data: {e}")


async def extract_recaptcha_score(engine: BrowserEngine) -> dict:
    """Extract Recaptcha Score from the page"""

    for i in range(3):
        try:
            recaptcha_data = await get_recaptcha_score_data(engine)
            if recaptcha_data.get("score") is not None:
                break
        except Exception as e:
            logger.warning(f"Attempt {i + 1} failed: {e}")

        try:
            await engine.reload_page()
            logger.info('Page reloaded')
        except Exception as reload_error:
            logger.warning(f"Page reload failed: {reload_error}")
    else:
        raise Exception("Failed to extract recaptcha score data after multiple attempts")

    return {
        'recaptcha_score': recaptcha_data.get("score", 0)
    }
