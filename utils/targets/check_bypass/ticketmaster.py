from engines.base import BrowserEngine


async def check_ticketmaster_bypass(engine: BrowserEngine) -> bool:
    element_found, element_html = await engine.query_selector('//abuse-component')

    return not element_found
