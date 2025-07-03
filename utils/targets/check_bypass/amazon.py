from engines.base import BrowserEngine


async def check_amazon_bypass(engine: BrowserEngine) -> bool:
    element_found, element_html = await engine.locator('[action="/errors/validateCaptcha"]')

    return not element_found
