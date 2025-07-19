import asyncio
import json
import logging

from engines.base import BrowserEngine
from utils.js_script import load_js_script

logger = logging.getLogger(__name__)

"""
! CreepJS disabled trust and bot scores for now - https://github.com/abrahamjuliot/creepjs/issues/292
! So we will return 0 for both scores
"""


async def get_creepjs_data(engine: BrowserEngine, tries: int = 10) -> dict:
    """
    Extract data (trust score, bot score, webrtc ip) from CreepJS page

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
    Extract CreepJS data: trust score, bot score, webrtc ip

    :param engine: BrowserEngine instance
    """

    try:
        creepjs_data = await get_creepjs_data(engine)
    except Exception as e:
        logger.error(f"Error getting CreepJS data for engine {engine.name}: {e}")
        creepjs_data = {}

    return {
        # 'creepjs_trust_score': creepjs_data.get("trust_score", 0),
        # 'creepjs_bot_score': creepjs_data.get("bot_score", 0) * 100,  # normalize value to 0-100
        'creepjs_trust_score': 0,
        'creepjs_bot_score': 0,
        'creepjs_webrtc_ip': creepjs_data.get("webrtc_ip", "")
    }
