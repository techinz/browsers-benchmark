from engines.base import BrowserEngine


async def check_cloudflare_bypass(engine: BrowserEngine) -> bool:
    cloudflare_title_found = False
    element_found1, element_html1 = await engine.locator("title")
    if element_html1 == 'Just a moment...':
        cloudflare_title_found = True

    # for non-english challenge page
    element_found2, element_html2 = await engine.locator('.main-content .core-msg.spacer.spacer-top')

    return not cloudflare_title_found and not element_found2
