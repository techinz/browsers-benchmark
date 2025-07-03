from typing import Dict, Optional

from engines.selenium_base import SeleniumBase


class SeleniumEngine(SeleniumBase):
    def __init__(
            self,
            name: str = "selenium-chrome__no_proxy",
            browser_type: str = "chrome",
            user_agent: Optional[str] = None,
            headless: bool = True,
            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        super().__init__(name, browser_type, user_agent, headless, proxy)
