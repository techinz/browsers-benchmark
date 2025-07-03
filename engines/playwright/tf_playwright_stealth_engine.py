import asyncio
import os
from typing import Dict, Optional

import psutil
from playwright.async_api import async_playwright, BrowserType
from playwright_stealth import stealth_async

from engines.playwright_base import PlaywrightBase
from utils.js_script import load_js_script
from utils.process import find_new_child_processes


class TfPlaywrightStealthEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "tf-playwright-stealth-chromium",
            browser_type: str = "chromium",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the TfPlaywrightStealthEngine with the given parameters

        :param name: Name of the engine instance
        :param browser_type: Type of browser to use (chromium, firefox, webkit)
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, browser_type, user_agent, headless, proxy)

    async def start(self) -> None:
        """Initialize and start the browser"""

        self._start_time = asyncio.get_event_loop().time()

        # get processes before browser is started
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        # initialize playwright
        self.playwright = await async_playwright().start()

        # launch browser type
        if self.browser_type not in ["chromium", "firefox", "webkit"]:
            raise ValueError(f"unsupported browser type: {self.browser_type}")

        browser_launcher: BrowserType = getattr(self.playwright, self.browser_type)
        self.browser = await browser_launcher.launch(headless=self.headless)

        # configure browser context
        context_options = {}

        if self.user_agent:
            context_options["user_agent"] = self.user_agent

        if self.proxy:
            context_options["proxy"] = {
                "server": f"{self.proxy['protocol']}://{self.proxy['host']}:{self.proxy['port']}",
            }
            if "username" in self.proxy and "password" in self.proxy:
                context_options["proxy"]["username"] = self.proxy["username"]
                context_options["proxy"]["password"] = self.proxy["password"]

        # create context and page
        self.context = await self.browser.new_context(**context_options)
        self.page = await self.context.new_page()

        await stealth_async(self.page)

        # monkey-patch attachShadow to force open mode for closed shadow DOM
        await self.context.add_init_script(await load_js_script('unlockShadowDom.js'))

        # track process for resource usage
        process_children_after = parent_process.children(recursive=True)
        process_children_filtered = find_new_child_processes(process_children_before, process_children_after)
        self.process_list = process_children_filtered
