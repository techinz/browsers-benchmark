import asyncio
import os
from typing import Dict, Optional

import psutil
from camoufox.async_api import AsyncCamoufox

from engines.playwright_base import PlaywrightBase
from utils.process import find_new_child_processes


class CamoufoxEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "camoufox",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the CamoufoxEngine with the given parameters

        :param name: Name of the engine instance
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless
        :param proxy: Proxy settings, if any
        """

        browser_type = 'firefox'  # camoufox only supports firefox
        super().__init__(name, browser_type, user_agent, headless, proxy)

        self.camoufox = None

    async def start(self) -> None:
        """Initialize and start the browser"""

        self._start_time = asyncio.get_event_loop().time()

        # get processes before browser is started
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        # configure browser options
        browser_options = {}

        if self.user_agent:
            browser_options["user_agent"] = self.user_agent

        if self.proxy:
            browser_options["proxy"] = {
                "server": f"{self.proxy['protocol']}://{self.proxy['host']}:{self.proxy['port']}",
            }
            if "username" in self.proxy and "password" in self.proxy:
                browser_options["proxy"]["username"] = self.proxy["username"]
                browser_options["proxy"]["password"] = self.proxy["password"]

        self.camoufox = AsyncCamoufox(headless=self.headless, geoip=True, **browser_options)
        await self.camoufox.start()

        self.browser = self.camoufox.browser

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
            if self.camoufox:
                await self.camoufox.__aexit__()
        except:
            pass
        self.camoufox = None

        self.process_list = None
