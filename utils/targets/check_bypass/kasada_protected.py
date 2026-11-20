from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_kasada_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the Kasada bypass is successful (Wizz Air)

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='div[data-test="main-page-container"]',
        min_wait_s=10
    )
