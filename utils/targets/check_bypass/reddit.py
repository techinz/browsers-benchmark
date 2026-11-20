from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_reddit_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the Reddit bypass is successful

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='shreddit-app',
        block_selector='a[href^="https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id="]'
    )
