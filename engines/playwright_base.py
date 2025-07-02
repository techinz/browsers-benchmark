import asyncio
import os
from typing import Dict, Optional, Any, Tuple

import psutil
from playwright.async_api import async_playwright, BrowserType

from config.settings import settings
from engines.base import BrowserEngine
from utils.js_script import load_js_script
from utils.process import find_new_child_processes


class PlaywrightBase(BrowserEngine):
    def __init__(
            self,
            name: str = "playwright-chrome",
            browser_type: str = "chromium",
            user_agent: Optional[str] = None,

            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
    ):
        super().__init__(name, proxy)
        self.browser_type = browser_type  # chromium, firefox, webkit
        self.headless = headless
        self.user_agent = user_agent

        self.playwright = None
        self.context = None
        self.page = None

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

        # monkey-patch attachShadow to force open mode for closed shadow DOM
        await self.context.add_init_script(await load_js_script('unlockShadowDom.js'))

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
            if self.playwright:
                await self.playwright.stop()
        except:
            pass
        self.playwright = None

        self.process_list = None

    async def navigate(self, url: str) -> Dict[str, Any]:
        """ Navigate to url and return page data """

        if not self.page:
            raise RuntimeError("Browser not started")

        start_time = asyncio.get_event_loop().time()
        response = await self.page.goto(url, timeout=settings.browser.page_load_timeout_ms)
        end_time = asyncio.get_event_loop().time()

        result = {
            "url": url,
            "status": response.status if response else None,
            "load_time": end_time - start_time,
            "success": response.ok if response else False,
            "headers": response.headers if response else {},
        }

        return result

    async def reload_page(self):
        """Reload the current page"""

        if not self.page:
            raise RuntimeError("Browser not started")

        await self.page.reload(timeout=settings.browser.page_load_timeout_ms)

    async def query_selector(self, selector: str) -> Tuple[bool, str]:
        """Query a selector and return found status and its content"""

        if not self.page:
            raise RuntimeError("browser not started")

        element_found = False
        element_html = ''

        element = await self.page.query_selector(selector)
        if element:
            element_found = True
            element_html: str = await element.inner_html()

        return element_found, element_html

    async def get_page_content(self) -> str:
        """Get current page html content"""

        if not self.page:
            raise RuntimeError("browser not started")

        return await self.page.content()

    async def execute_js(self, script: str) -> Any:
        """Execute javascript in browser context"""

        if not self.page:
            raise RuntimeError("browser not started")

        return await self.page.evaluate(script)

    async def screenshot(self, path: str) -> None:
        """Take a screenshot of the current page"""

        if not self.page:
            raise RuntimeError("browser not started")

        await self.page.screenshot(path=path)
