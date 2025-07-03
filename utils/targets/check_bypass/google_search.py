from engines.base import BrowserEngine


async def check_google_search_bypass(engine: BrowserEngine) -> bool:
    element_found, element_html = await engine.locator("div#search")

    return element_found
