import asyncio
import logging
import re

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def extract_ipify_data(engine: BrowserEngine) -> dict:
    """
    Extract ip from Ipify API page

    :param engine: BrowserEngine instance
    """

    await asyncio.sleep(5)  # ensure the page is fully loaded

    ip = '-'

    try:
        # read the ip from the raw html: firefox renders json in its own viewer (no <pre>), chrome wraps it in <pre>
        page_content = await engine.get_page_content()
        match = re.search(r'"ip"\s*:\s*"([0-9a-fA-F.:]+)"', page_content) or \
            re.search(r'\b((?:\d{1,3}\.){3}\d{1,3})\b', page_content)
        if match:
            ip = match.group(1)
    except Exception as e:
        logger.error(f"Error getting Ipify data for engine {engine.name}: {e}")

    return {
        'ip': ip
    }
