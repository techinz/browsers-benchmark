from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_perimeterx_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the PerimeterX (HUMAN Security) bypass is successful (Priceline)

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='a[href*="/hotels"]',
        block_selector='#px-captcha, #px-captcha-modal',
        min_wait_s=10
    )
