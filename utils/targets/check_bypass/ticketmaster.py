from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_ticketmaster_bypass(engine: BrowserEngine) -> bool:
    """
    Check if TicketMaster captcha (Imperva) bypass is successful

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='#main-content',
        block_selector='abuse-component'
    )
