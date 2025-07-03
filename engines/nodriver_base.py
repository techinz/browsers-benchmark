import asyncio
import logging
import os
from typing import Dict, Optional, Any, Tuple

import nodriver as uc
import psutil

from config.settings import settings
from engines.base import BrowserEngine, NavigationResult
from utils.process import find_new_child_processes

logger = logging.getLogger(__name__)


class NoDriverBase(BrowserEngine):
    def __init__(
            self,
            name: str = "nodriver-chrome",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the NoDriverBase with the given parameters

        :param name: Name of the engine instance
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, proxy)
        self.user_agent = user_agent
        self.headless = headless

        self.browser: Optional[uc.Browser] = None
        self.page: Optional[uc.Tab] = None

    @property
    def supported_proxy_protocols(self) -> list[str]:
        return ["socks5"]

    async def start(self) -> None:
        """Initialize and start the browser"""

        self._start_time = asyncio.get_event_loop().time()

        # get processes before browser is started
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        browser_args = []

        if self.headless:
            browser_args.extend(['--headless=new'])  # use new headless mode

        if self.user_agent:
            browser_args.append(f'--user-agent={self.user_agent}')

        try:
            # start browser with nodriver
            self.browser = await uc.start(
                headless=self.headless,
                browser_args=browser_args,
                user_data_dir=None,  # use temporary profile
                sandbox=False
            )

            # create context with proxy configuration if provided
            if self.proxy:
                if self.proxy.get('protocol') != 'socks5':
                    raise ValueError(
                        "NoDriver only supports SOCKS5 proxies. Please place some SOCKS5 proxy in the 'proxies' file.")

                proxy_server = f"{self.proxy['host']}:{self.proxy['port']}"

                # add protocol prefix
                protocol = self.proxy.get('protocol', 'socks5')
                proxy_url = f"{protocol}://{proxy_server}"

                # add authentication if provided
                if self.proxy.get('username') and self.proxy.get('password'):
                    proxy_url = f"{protocol}://{self.proxy['username']}:{self.proxy['password']}@{proxy_server}"

                # create proxied context
                self.page = await self.browser.create_context(
                    proxy_server=proxy_url
                )
                logger.info(f"Created proxied context: {proxy_url}")
            else:
                self.page = self.browser.main_tab

            logger.info(f"NoDriver browser started successfully: {self.name}")
        except Exception as e:
            logger.error(f"Failed to start NoDriver browser: {e}")
            raise

        # track process for resource usage
        process_children_after = parent_process.children(recursive=True)
        process_children_filtered = find_new_child_processes(process_children_before, process_children_after)
        self.process_list = process_children_filtered

    async def stop(self) -> None:
        """Stop the browser and clean up resources"""

        try:
            if self.browser:
                self.browser.stop()
        except Exception as e:
            logger.debug(f"Error stopping browser: {e}")

        self.browser = None
        self.page = None
        self.process_list = None

    async def navigate(self, url: str) -> NavigationResult:
        """
        Navigate to url and return page data

        :param url: URL to navigate to
        """

        if not self.page:
            raise RuntimeError("Browser not started")

        start_time = asyncio.get_event_loop().time()

        try:
            await asyncio.wait_for(self.page.get(url),
                                   timeout=settings.browser.page_load_timeout_s)  # because nodriver doesn't support timeout natively (as far as I know)
            success = True
        except Exception as e:
            success = False

        end_time = asyncio.get_event_loop().time()

        result: NavigationResult = {
            "url": url,
            "load_time": end_time - start_time,
            "success": success,
            "headers": {},  # nodriver doesn't provide direct access to response headers
        }

        return result

    async def reload_page(self) -> NavigationResult:
        """Reload the current page"""

        if not self.page:
            raise RuntimeError("Browser not started")

        start_time = asyncio.get_event_loop().time()

        try:
            await self.page.reload()
            success = True
        except Exception:
            success = False

        end_time = asyncio.get_event_loop().time()

        result: NavigationResult = {
            "url": self.page.url if self.page else "",
            "load_time": end_time - start_time,
            "success": success,
            "headers": {},
        }

        return result

    async def locator(self, css_selector: str) -> Tuple[bool, str]:
        """
        Locate a selector and return found status and its content

        :param css_selector: CSS selector to locate the element
        """

        if not self.page:
            raise RuntimeError("Browser not started")

        element_found = False
        element_html = ''

        try:
            element = await self.page.select(css_selector)
            if element:
                element_found = True
                try:
                    # get innerHTML or text content
                    inner_html_result = await self.page.evaluate(f"document.querySelector('{css_selector}').innerHTML")
                    if isinstance(inner_html_result, str) and inner_html_result:
                        element_html = inner_html_result
                    else:
                        text_result = await self.page.evaluate(f"document.querySelector('{css_selector}').textContent")
                        element_html = text_result if isinstance(text_result, str) else ""
                except Exception:
                    # fallback to getting text if available
                    try:
                        element_html = str(element.text) if hasattr(element, 'text') and element.text else ""
                    except Exception:
                        element_html = ""
        except Exception:
            pass

        return element_found, element_html

    async def get_page_content(self) -> str:
        """Get current page html content"""

        if not self.page:
            raise RuntimeError("Browser not started")

        try:
            return await self.page.get_content()
        except Exception as e:
            logger.error(f"Failed to get page content: {e}")
            return ""

    async def execute_js(self, script: str) -> Any:
        """
        Execute javascript in browser context

        :param script: JavaScript code to execute
        """

        if not self.page:
            raise RuntimeError("Browser not started")

        try:
            return await self.page.evaluate(f"(() => {{\n{script}\n}})();")  # wrap script in IIFE
        except Exception as e:
            logger.error(f"Failed to execute JavaScript: {e}")
            return None

    async def screenshot(self, path: str) -> None:
        """
        Take a screenshot of the current page

        :param path: Path to save the screenshot
        """

        if not self.page:
            raise RuntimeError("Browser not started")

        # ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            await self.page.save_screenshot(path)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

    def get_memory_usage(self) -> int:
        """Get memory usage of browser processes in MB"""

        if not self.process_list:
            return 0

        total_memory = 0
        for process in self.process_list:
            try:
                if process.is_running():
                    memory_info = process.memory_info()
                    total_memory += memory_info.rss  # Resident Set Size in bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return total_memory // (1024 * 1024)  # convert to MB

    def get_cpu_usage(self) -> float:
        """Get CPU usage percentage of browser processes"""

        if not self.process_list:
            return 0.0

        total_cpu = 0.0
        for process in self.process_list:
            try:
                if process.is_running():
                    total_cpu += process.cpu_percent()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return total_cpu
