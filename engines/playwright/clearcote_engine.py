import asyncio
import os
from typing import Dict, Optional, Literal

import psutil
from clearcote.async_api import launch

from config.settings import settings
from engines.playwright_base import PlaywrightBase
from utils.js_script import load_js_script
from utils.process import find_new_child_processes


class ClearcoteEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "clearcote",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the ClearcoteEngine with the given parameters

        :param name: Name of the engine instance
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless mode
        :param proxy: Proxy settings, if any

        Runs the open build without a key. Set CLEARCOTE_LICENSE_KEY to run the licensed build.
        """

        browser_type: Literal['chromium', 'firefox', 'webkit'] = 'chromium'
        super().__init__(name, browser_type, user_agent, headless, proxy)

    async def start(self) -> None:
        """Initialize and start the browser"""

        self._start_time = asyncio.get_event_loop().time()

        # get processes before browser is started
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        proxy = None
        if self.proxy:
            proxy = {
                "server": f"{self.proxy['protocol']}://{self.proxy['host']}:{self.proxy['port']}",
            }

            if "username" in self.proxy and "password" in self.proxy:
                proxy["username"] = self.proxy["username"]
                proxy["password"] = self.proxy["password"]

        # configure browser options (geoip matches timezone/locale to the proxy's exit)
        browser_options = {
            "headless": self.headless,
            "geoip": True,
        }

        if proxy:
            browser_options["proxy"] = proxy

        self.browser = await launch(**browser_options)

        # configure context options
        context_options = {}

        if self.user_agent:
            context_options["user_agent"] = self.user_agent

        # create context and page
        self.context = await self.browser.new_context(**context_options)
        self.page = await self.context.new_page()

        self.page.set_default_timeout(settings.browser.action_timeout_s * 1000)
        self.page.set_default_navigation_timeout(settings.browser.page_load_timeout_s * 1000)

        # monkey-patch attachShadow to force open mode for closed shadow DOM
        await self.context.add_init_script(await load_js_script('unlockShadowDom.js'))

        # track process for resource usage
        process_children_after = parent_process.children(recursive=True)
        process_children_filtered = find_new_child_processes(process_children_before, process_children_after)
        self.process_list = process_children_filtered
