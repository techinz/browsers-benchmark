import asyncio
import logging

from engines.base import BrowserEngine
from utils.js_script import load_js_script

logger = logging.getLogger(__name__)


async def get_recaptcha_score_data(engine: BrowserEngine, tries: int = 10) -> dict:
    """ Extract data from Recaptcha Score Detector page """

    try:
        for i in range(tries):
            await asyncio.sleep(5)

            data = await engine.execute_js(await load_js_script('parseRecaptchaScore.js'))
            if data and data.get('recaptcha_score') is not None:
                break
        else:
            raise Exception("Failed to extract recaptcha score data (recaptcha score not found, out of tries)")

        return data
    except Exception as e:
        raise Exception(f"Failed to extract recaptcha score data: {e}")


async def extract_recaptcha_score(engine: BrowserEngine) -> dict:
    """ Extract Recaptcha Score from the page """

    try:
        recaptcha_data = await get_recaptcha_score_data(engine)
    except Exception as e:
        logger.error(f"Error getting Recaptcha Score data for engine {engine.name}: {e}")
        recaptcha_data = {}

    return {
        'recaptcha_score': recaptcha_data.get("recaptcha_score", 0)
    }
