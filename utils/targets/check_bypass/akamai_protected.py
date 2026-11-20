from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_akamai_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the Akamai Bot Manager bypass is successful (Mr Porter)

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='icon[aria-label="Search"]'
    )
