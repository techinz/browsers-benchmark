from engines.base import BrowserEngine


BOT_REDIRECT_MARKER = "verify/traffic/error"


async def check_shopee_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the Shopee Singapore traffic verification bypass is successful.

    Shopee bot detection redirects caught traffic to a URL containing
    ``verify/traffic/error``. Unknown or unreadable current URL state fails
    closed rather than counting as a bypass.

    :param engine: BrowserEngine instance
    """

    try:
        current_url = await engine.execute_js("return window.location.href;")
    except Exception:
        return False

    if not isinstance(current_url, str):
        return False

    normalized_url = current_url.strip().lower()
    if not normalized_url:
        return False

    return BOT_REDIRECT_MARKER not in normalized_url
