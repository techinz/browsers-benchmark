import asyncio
import logging

from engines.base import BrowserEngine
from utils.js_script import load_js_script

logger = logging.getLogger(__name__)


async def get_2ip_data(engine: BrowserEngine, tries: int = 10) -> dict:
    """ Extract data from 2IP page """

    try:
        for i in range(tries):
            await asyncio.sleep(5)

            data = await engine.execute_js(await load_js_script('parse2ip.js'))
            if data and data.get('ip') is not None:
                break
        else:
            raise Exception("Failed to extract 2ip data (ip not found, out of tries)")

        return data
    except Exception as e:
        raise Exception(f"Failed to extract 2ip data: {e}")


async def extract_2ip_data(engine: BrowserEngine) -> dict:
    """ Extract 2IP from the page """

    await asyncio.sleep(5)  # ensure the page is fully loaded

    try:
        twoip_data = await get_2ip_data(engine)
    except Exception as e:
        logger.error(f"Error getting 2IP data for engine {engine.name}: {e}")
        twoip_data = {}

    return {
        'ip': twoip_data.get("ip", 0)
    }
