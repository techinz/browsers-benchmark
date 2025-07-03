from engines.base import BrowserEngine


async def check_amazon_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the Amazon captcha bypass is successful

    :param engine: BrowserEngine instance
    """

    element_found, element_html = await engine.locator('[action="/errors/validateCaptcha"]')

    return not element_found
