import asyncio
import logging

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def check_datadome2_bypass(engine: BrowserEngine, tries: int = 20) -> bool:
    """
    Check if datadome bypass is successful

    :param engine: BrowserEngine instance
    :param tries: Number of attempts to check
    """

    await asyncio.sleep(15)  # time to load

    # it returns no content for some time and only then renders captcha or page
    bypass = False
    for i in range(tries):
        target_page_loaded_found, target_page_loaded_html = await engine.locator('#account-link')
        captcha_loaded_found, captcha_loaded_html = await engine.locator(
            '[id*="ddChallengeContainer"]')

        page_content = await engine.get_page_content()

        captcha_loaded_found2, captcha_loaded_html2 = False, ''
        if '<html><head><title>403 Forbidden</title></head>' in page_content:
            captcha_loaded_found2, captcha_loaded_html2 = True, '<title>403 Forbidden</title>'

        if any((target_page_loaded_found, captcha_loaded_found, captcha_loaded_found2)):
            bypass = not (captcha_loaded_found or captcha_loaded_found2)
            break

        logger.info("Datadome bypass 2 not determined yet, retrying...")

        await asyncio.sleep(2.5)

    return bypass
