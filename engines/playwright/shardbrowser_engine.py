import asyncio
import os
import shutil
import tempfile
from typing import Dict, Optional

import psutil
from patchright.async_api import async_playwright
from shardx import ShardX

from config.settings import settings
from engines.playwright_base import PlaywrightBase
from utils.js_script import load_js_script
from utils.process import find_new_child_processes


class ShardBrowserEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "shardbrowser",
            headless: bool = False,
            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the ShardBrowserEngine with the given parameters

        Every start creates a fresh Windows profile from the bundled fingerprint library
        and drops it on stop, the same way the AdsPower engine does with its profiles.

        :param name: Name of the engine instance
        :param headless: Whether to run the browser in headless mode
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, "chromium", None, headless, proxy)
        self._profiles_dir: Optional[str] = None
        self._session = None

    @property
    def supported_proxy_protocols(self) -> list[str]:
        return ["http", "socks5"]

    def _proxy_url(self) -> Optional[str]:
        if not self.proxy:
            return None
        auth = ""
        if "username" in self.proxy and "password" in self.proxy:
            auth = f"{self.proxy['username']}:{self.proxy['password']}@"
        return f"{self.proxy['protocol']}://{auth}{self.proxy['host']}:{self.proxy['port']}"

    async def start(self) -> None:
        """Create a profile, launch the ShardBrowser engine and connect via CDP"""

        self._start_time = asyncio.get_event_loop().time()

        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        self._profiles_dir = tempfile.mkdtemp(prefix="shardbrowser-")
        sdk = ShardX(profiles_dir=self._profiles_dir)
        profile = await asyncio.to_thread(sdk.create_profile, platform="Win")
        self._session = await asyncio.to_thread(
            sdk.launch, profile, proxy=self._proxy_url(), cdp=True, headless=self.headless
        )
        if not self._session.cdp_url:
            raise RuntimeError("ShardBrowser did not expose a CDP endpoint")

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.connect_over_cdp(self._session.cdp_url)
        self.context = self.browser.contexts[0]

        await self.context.add_init_script(await load_js_script('unlockShadowDom.js'))

        self.page = await self.context.new_page()
        self.page.set_default_timeout(settings.browser.action_timeout_s * 1000)
        self.page.set_default_navigation_timeout(settings.browser.page_load_timeout_s * 1000)

        process_children_after = parent_process.children(recursive=True)
        self.process_list = find_new_child_processes(process_children_before, process_children_after)

    async def stop(self) -> None:
        """Close the page, disconnect, stop the engine and delete the profile"""

        try:
            if self.page:
                await self.page.close()
        except:
            pass
        self.page = None

        try:
            if self.browser:
                await self.browser.close()
        except:
            pass
        self.browser = None
        self.context = None

        try:
            if self.playwright:
                await self.playwright.stop()
        except:
            pass
        self.playwright = None

        if self._session:
            await asyncio.to_thread(self._session.stop)
            self._session = None

        if self._profiles_dir:
            shutil.rmtree(self._profiles_dir, ignore_errors=True)
            self._profiles_dir = None

        self.process_list = None
