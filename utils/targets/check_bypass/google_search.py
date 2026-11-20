from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_google_search_bypass(engine: BrowserEngine) -> bool:
    """
    Check if Google Search captcha (recaptcha) bypass is successful

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='div#search'
    )
