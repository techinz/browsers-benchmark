from engines.base import BrowserEngine


async def check_cloudflare_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the cloudflare bypass is successful

    :param engine: BrowserEngine instance
    """

    element_found1, element_html1 = await engine.locator('[title="Just a moment..."]')

    # for non-english challenge page
    element_found2, element_html2 = await engine.locator('.main-content .core-msg.spacer.spacer-top')

    return not element_found1 and not element_found2
