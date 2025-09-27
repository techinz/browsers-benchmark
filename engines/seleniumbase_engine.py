import asyncio
import logging
import os
from typing import Dict, Optional

import psutil
from seleniumbase.undetected import cdp_driver
from seleniumbase.undetected.cdp_driver.browser import Browser
from seleniumbase.undetected.cdp_driver.tab import Tab

from config.settings import settings
from engines.nodriver_base import NoDriverBase
from utils.process import find_new_child_processes

logger = logging.getLogger(__name__)


class SeleniumBaseCDPEngine(NoDriverBase):
    def __init__(
            self,
            name: str = 'seleniumbase-cdp-chrome',
            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        # Always use headless=False for SeleniumBase CDP engine
        super().__init__(name, headless=False, proxy=proxy, **kwargs)

        # Explicitly type the browser and page with SeleniumBase types
        self.browser: Optional[Browser] = None
        self.page: Optional[Tab] = None

    @property
    def supported_proxy_protocols(self) -> list[str]:
        # SeleniumBase's CDP driver supports multiple proxy protocols
        # as seen in seleniumbase/core/proxy_helper.py
        return ["http", "https", "socks4", "socks5"]

    async def _start_seleniumbase(self, proxy_str=None):
        self.browser = await asyncio.wait_for(
            cdp_driver.cdp_util.start_async(proxy=proxy_str),
            timeout=settings.browser.action_timeout_s
        )
        # workaround to init proxy setup in seleniumbase
        self.page = await self.browser.get("about:blank")

    def _build_proxy_str(self) -> str | None:
        if not self.proxy:
            return None

        protocol = self.proxy.get('protocol')
        host = self.proxy.get('host')
        port = self.proxy.get('port')
        username = self.proxy.get('username')
        password = self.proxy.get('password')

        if protocol and protocol not in self.supported_proxy_protocols:
            raise ValueError(
                f"Unsupported proxy protocol: {protocol}. SeleniumBase CDP supports: {self.supported_proxy_protocols}")

        if username and password:
            proxy_str = f"{username}:{password}@{protocol}://{host}:{port}"
        else:
            proxy_str = f"{protocol}://{host}:{port}"
        logger.info(f"Using proxy: {proxy_str}")

        return proxy_str

    async def start(self) -> None:
        """Start the SeleniumBase CDP browser"""
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        proxy_str = self._build_proxy_str()
        await self._start_seleniumbase(proxy_str)

        # track process for resource usage
        process_children_after = parent_process.children(recursive=True)
        process_children_filtered = find_new_child_processes(process_children_before, process_children_after)
        self.process_list = process_children_filtered

    async def stop(self) -> None:
        """Stop the SeleniumBase CDP browser"""
        if self.browser:
            # SeleniumBase's stop method is synchronous, not async
            self.browser.stop()

        self.browser = None
        self.page = None
        self.process_list = None
