from typing import Dict, Optional, Literal

from engines.playwright_base import PlaywrightBase


class PlaywrightEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "playwright-chrome",
            browser_type: Literal['firefox', 'chromium', 'webkit'] = "chromium",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the PlaywrightEngine with the given parameters

        :param name: Name of the engine instance
        :param browser_type: Type of browser to use (chromium, firefox, webkit)
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, browser_type, user_agent, headless, proxy)
