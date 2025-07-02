from typing import Dict, Optional

from engines.playwright_base import PlaywrightBase


class PlaywrightEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "playwright-chrome",
            browser_type: str = "chromium",
            user_agent: Optional[str] = None,

            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
    ):
        super().__init__(name, browser_type, user_agent, headless, proxy)
