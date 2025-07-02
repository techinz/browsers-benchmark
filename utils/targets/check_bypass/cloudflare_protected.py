from engines.base import BrowserEngine


async def check_cloudflare_bypass(engine: BrowserEngine) -> bool:
    element_found1, element_html1 = await engine.locator("//title[contains(text(), 'Just a moment...')]")
    # for non-english challenge page
    element_found2, element_html2 = await engine.locator(
        '//div[@class="main-content"]//div[@class="core-msg spacer spacer-top"]')

    return not element_html1 and not element_html2
