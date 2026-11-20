from engines.base import BrowserEngine
from utils.targets.check_bypass.page_state import wait_for_bypass


async def check_amazon_bypass(engine: BrowserEngine) -> bool:
    """
    Check if the Amazon captcha bypass is successful (product page is shown, not a captcha/checkpoint page)

    :param engine: BrowserEngine instance
    """

    return await wait_for_bypass(
        engine,
        success_selector='#productTitle',
        block_selector='form[action*="validateCaptcha"], #checkpointForm'
    )
