import abc
import time
from typing import Dict, Optional, Any, TypedDict, Tuple

import psutil


class NavigationResult(TypedDict):
    """
    Result of a navigation operation

    :param url: URL of the page after navigation
    :param load_time: Time taken to load the page in seconds
    :param success: Whether the navigation was successful
    :param headers: Response headers from the navigation request (not always available)
    """

    url: str
    load_time: float
    success: bool
    headers: Dict[str, str]


class BrowserEngine(abc.ABC):
    """
    Base class for all browser engine implementations

    :param name: Name of the browser engine.

    :param proxy: Optional proxy settings for the browser.
    :param proxy['protocol']: Proxy protocol (e.g., 'http', 'socks5').
    :param proxy['host']: Proxy host.
    :param proxy['port']: Proxy port.
    :param proxy['username']: Optional proxy username.
    :param proxy['password']: Optional proxy password.
    """

    def __init__(self, name: str, proxy: Optional[Dict[str, str]] = None):
        self.name = name
        self.proxy = proxy
        self.process_list = []
        self.browser = None
        self._start_time = None

    @property
    @abc.abstractmethod
    def supported_proxy_protocols(self) -> list[str]:
        """List of supported proxy protocols for this engine"""
        pass

    @abc.abstractmethod
    async def start(self) -> None:
        """Initialize and start the browser"""
        pass

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop the browser and clean up resources"""
        pass

    async def restart(self) -> None:
        """Recreate and restart the browser engine"""

        await self.stop()
        await self.start()

    @abc.abstractmethod
    async def navigate(self, url: str) -> NavigationResult:
        """
        Navigate to url and return page data

        :param url: URL to navigate to
        """

        pass

    @abc.abstractmethod
    async def reload_page(self) -> NavigationResult:
        """Reload the current page"""
        pass

    @abc.abstractmethod
    async def locator(self, css_selector: str) -> Tuple[bool, str]:
        """
        Locate a selector and return its content

        :param css_selector: CSS selector to locate element
        """

        pass

    @abc.abstractmethod
    async def get_page_content(self) -> str:
        """Get current page html content"""
        pass

    @abc.abstractmethod
    async def execute_js(self, script: str) -> Any:
        """
        Execute javascript in browser context

        :param script: JavaScript code to execute
        """

        pass

    @abc.abstractmethod
    async def screenshot(self, path: str) -> None:
        """
        Take a screenshot of the current page

        :param path: Path to save the screenshot
        """

        pass

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""

        if not self.process_list:
            return 0.0

        total_memory = 0.0
        for proc in self.process_list:
            try:
                total_memory += proc.memory_info().rss / 1024 / 1024
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return total_memory

    def get_cpu_usage(self) -> float:
        """Get current cpu usage percentage"""

        if not self.process_list:
            return 0.0

        total_cpu = 0.0
        for proc in self.process_list:
            try:
                total_cpu += proc.cpu_percent(interval=0.05)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return total_cpu

    def get_runtime(self) -> float:
        """Get runtime in seconds since browser start"""

        if not self._start_time:
            return 0.0
        return time.time() - self._start_time
