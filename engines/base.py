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

    def get_memory_usage(self) -> int:
        """Get current memory usage in MB"""

        if not self.process_list:
            return 0

        total_memory = 0
        for proc in self.process_list:
            try:
                if proc.is_running():
                    memory_info = proc.memory_info()
                    total_memory += memory_info.rss  # Resident Set Size in bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return total_memory // (1024 * 1024)  # convert to MB

    def get_cpu_usage(self) -> float:
        """Get current cpu usage percentage"""

        if not self.process_list:
            return 0.0

        total_cpu = 0.0
        valid_processes = 0

        for proc in self.process_list:
            try:
                if proc.is_running():
                    # Use interval=None to get non-blocking CPU percent
                    # This returns the CPU usage since the last call
                    cpu_usage = proc.cpu_percent(interval=None)

                    # If this is the first call and returns 0, make a second call with interval
                    if cpu_usage == 0.0:
                        # Small delay and second measurement for accuracy
                        import time
                        time.sleep(0.1)
                        cpu_usage = proc.cpu_percent(interval=0.1)

                    total_cpu += cpu_usage
                    valid_processes += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return total_cpu

    def get_runtime(self) -> float:
        """Get runtime in seconds since browser start"""

        if not self._start_time:
            return 0.0
        return time.time() - self._start_time
