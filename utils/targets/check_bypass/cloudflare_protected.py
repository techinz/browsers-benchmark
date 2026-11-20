from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_cloudflare_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the cloudflare bypass is successful (the Discourse forum behind the challenge is rendered)

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='#main-outlet'
    )
