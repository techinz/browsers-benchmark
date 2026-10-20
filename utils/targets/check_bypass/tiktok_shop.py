from engines.base import BrowserEngine


async def _count(engine: BrowserEngine, selector: str) -> int:
    """Return element count via JS to avoid strict-mode violations."""
    try:
        return await engine.execute_js(
            f"return document.querySelectorAll({repr(selector)}).length"
        )
    except Exception:
        return 0


async def check_tiktok_shop_bypass(engine: BrowserEngine) -> bool:
    """
    Check if TikTok Shop product page bypass is successful.

    Success: product content is visible (price, title, or product container).
    Failure: CAPTCHA, bot detection, or 403/block page.
    """

    captcha = await _count(engine, '.captcha_verify_container')
    captcha2 = await _count(engine, '[class*="secsdk-captcha"]')
    block = await _count(engine, '[id*="challenge"]')

    if captcha or captcha2 or block:
        return False

    price = await _count(engine, '[data-testid="product-price"]')
    price2 = await _count(engine, '.price-area')
    title = await _count(engine, '[data-testid="product-title"]')
    title2 = await _count(engine, '.product-title-container')
    pdp = await _count(engine, '.pdp-scroll-container')

    return bool(price or price2 or title or title2 or pdp)
