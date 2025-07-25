import asyncio

from engines.base import BrowserEngine


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

        if target_page_loaded_found or captcha_loaded_found:
            bypass = not captcha_loaded_found
            break

        await asyncio.sleep(2.5)

    return bypass
