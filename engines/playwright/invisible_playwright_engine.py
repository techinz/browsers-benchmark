import asyncio
import os
from typing import Dict, Optional, Literal

import psutil
from invisible_playwright.async_api import InvisiblePlaywright

from engines.playwright_base import PlaywrightBase
from utils.process import find_new_child_processes


class InvisiblePlaywrightEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "invisible-playwright",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the InvisiblePlaywrightEngine with the given parameters

        invisible_playwright drives a patched Firefox whose fingerprint is set
        at the engine/source level, so the browser_type is always firefox.

        :param name: Name of the engine instance
        :param user_agent: Custom user agent string (left to the generated
            profile by default to keep the fingerprint consistent)
        :param headless: Whether to run the browser in headless
        :param proxy: Proxy settings, if any
        """

        browser_type: Literal['chromium', 'firefox', 'webkit'] = 'firefox'  # invisible_playwright only supports firefox
        super().__init__(name, browser_type, user_agent, headless, proxy)

        self.invisible = None

    async def start(self) -> None:
        """Initialize and start the browser"""

        self._start_time = asyncio.get_event_loop().time()

        # get processes before browser is started
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        # configure browser options
        browser_options = {"headless": self.headless}

        # user agent / locale / timezone are derived from the generated profile
        # (and the proxy egress) to stay consistent, so only override the UA if
        # one is explicitly provided
        if self.user_agent:
            browser_options["extra_prefs"] = {"general.useragent.override": self.user_agent}

        if self.proxy:
            server = f"{self.proxy['protocol']}://{self.proxy['host']}:{self.proxy['port']}"
            proxy_options = {"server": server}
            if "username" in self.proxy and "password" in self.proxy:
                proxy_options["username"] = self.proxy["username"]
                proxy_options["password"] = self.proxy["password"]
            browser_options["proxy"] = proxy_options

        self.invisible = InvisiblePlaywright(**browser_options)
        self.browser = await self.invisible.__aenter__()

        # create context and page
        self.context = await self.browser.new_context()
        self.page = await self.browser.new_page()

        # track process for resource usage
        process_children_after = parent_process.children(recursive=True)
        process_children_filtered = find_new_child_processes(process_children_before, process_children_after)
        self.process_list = process_children_filtered

    async def stop(self) -> None:
        """Stop the browser and clean up resources"""

        try:
            if self.page:
                await self.page.close()
        except:
            pass
        self.page = None

        try:
            if self.context:
                await self.context.close()
        except:
            pass
        self.context = None

        try:
            if self.browser:
                await self.browser.close()
        except:
            pass
        self.browser = None

        try:
            if self.invisible:
                await self.invisible.__aexit__(None, None, None)
        except:
            pass
        self.invisible = None

        self.process_list = None
