import asyncio
import logging
import re

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def get_recaptcha_score_data(engine: BrowserEngine, tries: int = 5) -> dict:
    """
    Extract data from Recaptcha Score Detector page

    :param engine: BrowserEngine instance
    :param tries: Number of attempts to extract data
    """

    try:
        for i in range(tries):
            await asyncio.sleep(5)

            element_found, element_html = await engine.locator('div.row')
            if not element_found:
                continue

            score_match = re.search(r'Your score is:\s*([\d.]+)', element_html)
            if not score_match:
                continue

            data = {"score": float(score_match.group(1))}

            break
        else:
            raise Exception("Failed to extract recaptcha score data (recaptcha score not found, out of tries)")

        return data
    except Exception as e:
        raise Exception(f"Failed to extract recaptcha score data: {e}")


async def extract_recaptcha_score(engine: BrowserEngine) -> dict:
    """
    Extract Recaptcha Score from the page

    :param engine: BrowserEngine instance
    """

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
