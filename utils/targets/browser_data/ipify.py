import asyncio
import json
import logging

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def extract_ipify_data(engine: BrowserEngine) -> dict:
    """ Extract ip from Ipify API page """

    await asyncio.sleep(5)  # ensure the page is fully loaded

    ip = '-'

    try:
        element_found, element_html = await engine.locator('pre')
        if element_found:
            json_content = json.loads(element_html)
            ip = json_content.get('ip', '-')
    except Exception as e:
        logger.error(f"Error getting Ipify data for engine {engine.name}: {e}")

    return {
        'ip': ip
    }
