import asyncio
import logging

from engines.base import BrowserEngine

logger = logging.getLogger(__name__)


async def check_datadome_bypass(engine: BrowserEngine, tries: int = 20) -> bool:
    """
    Check if datadome bypass is successful

    :param engine: BrowserEngine instance
    :param tries: Number of attempts to check
    """

    await asyncio.sleep(10)  # time to load

    # it returns no content for some time and only then renders captcha or page
    bypass = False
    for i in range(tries):
        target_page_loaded_found, target_page_loaded_html = await engine.locator('#top')
        captcha_loaded_found, captcha_loaded_html = await engine.locator(
            'iframe[title*="Datadome"], iframe[title*="DataDome CAPTCHA"]')
        captcha_loaded_found2, captcha_loaded_html2 = await engine.locator(
            'iframe[title="DataDome Device Check"]')

        page_content = await engine.get_page_content()

        captcha_loaded_found3, captcha_loaded_html3 = False, ''
        if '<span>This site can’t be reached</span>' in page_content:
            captcha_loaded_found3, captcha_loaded_html3 = True, '<span>This site can’t be reached</span>'

        captcha_loaded_found4, captcha_loaded_html4 = False, ''
        if '<body>' not in page_content:
            captcha_loaded_found4, captcha_loaded_html4 = True, '<body> not in page content'

        if any((target_page_loaded_found, captcha_loaded_found, captcha_loaded_found2,
                captcha_loaded_html3, captcha_loaded_found4)):
            bypass = not (
                    captcha_loaded_found or captcha_loaded_found2 or captcha_loaded_html3 or captcha_loaded_found4)
            break

        logger.info("Datadome bypass not determined yet, retrying...")

        await asyncio.sleep(2.5)

    return bypass
