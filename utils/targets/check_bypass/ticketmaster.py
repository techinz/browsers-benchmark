from engines.base import BrowserEngine


async def check_ticketmaster_bypass(engine: BrowserEngine) -> bool:
    """
    Check if TicketMaster captcha (Imperva) bypass is successful

    :param engine: BrowserEngine instance
    """

    element_found, element_html = await engine.locator('abuse-component')

    return not element_found
