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
        """
        Initialize the SeleniumEngine with the given parameters

        :param name: Name of the engine instance
        :param browser_type: Type of browser to use (chrome, firefox)
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, browser_type, user_agent, headless, proxy)
