import asyncio
import json
import logging

from engines.base import BrowserEngine
from utils.js_script import load_js_script

logger = logging.getLogger(__name__)


async def get_creepjs_data(engine: BrowserEngine, tries: int = 10) -> dict:
    """
    Extract data (webrtc ip) from CreepJS page

    :param engine: BrowserEngine instance
    :param tries: Number of attempts to extract data
    """

    try:
        for i in range(tries):
            await asyncio.sleep(5)

            data = await engine.execute_js(await load_js_script('parseCreepJS.js'))
            data = json.loads(data) if data and isinstance(data, str) else data
            if data and data.get('webrtc_ip') is not None:
                break
        else:
            raise Exception("Failed to extract CreepJS data")

        return data
    except Exception as e:
        raise Exception(f"Failed to extract CreepJS data: {e}")


async def extract_creepjs_data(engine: BrowserEngine) -> dict:
    """
    Extract CreepJS data: webrtc ip (headless/stealth detection is a separate bot detection test)

    :param engine: BrowserEngine instance
    """

    try:
        creepjs_data = await get_creepjs_data(engine)
    except Exception as e:
        logger.error(f"Error getting CreepJS data for engine {engine.name}: {e}")
        creepjs_data = {}

    return {
        'creepjs_webrtc_ip': creepjs_data.get("webrtc_ip", "")
    }
