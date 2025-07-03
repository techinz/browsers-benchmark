from engines.base import BrowserEngine


async def check_google_search_bypass(engine: BrowserEngine) -> bool:
    """
    Check if Google Search captcha (recaptcha) bypass is successful

    :param engine: BrowserEngine instance
    """

    element_found, element_html = await engine.locator("div#search")

    return element_found
