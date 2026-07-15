import asyncio
import logging
import os
from typing import Dict, Optional, Any, Tuple

from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
import psutil

from config.settings import settings
from engines.base import BrowserEngine, NavigationResult
from utils.process import find_new_child_processes

logger = logging.getLogger(__name__)


class PydollEngine(BrowserEngine):
    def __init__(
            self,
            name: str = "pydoll-chrome",
            user_agent: Optional[str] = None,
            headless: bool = True,
            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the PydollEngine with the given parameters

        :param name: Name of the engine instance
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless mode
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, proxy)
        self.user_agent = user_agent
        self.headless = headless

        self.browser: Optional[Chrome] = None
        self.page = None

    def _extract_value_from_cdp(self, result: Any) -> Any:
        # CDP nests exactly two "result" layers:
        # {"result": {"result": {"type": "...", "value": "..."}}}
        # 1st "result" = CDP response wrapper, 2nd "result" = RemoteObject
        if isinstance(result, dict) and "result" in result:
            result = result["result"]
        if isinstance(result, dict) and "result" in result:
            result = result["result"]
        if isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    @property
    def supported_proxy_protocols(self) -> list[str]:
        return ["http", "https"]

    async def start(self) -> None:
        """Initialize and start the browser"""

        self._start_time = asyncio.get_event_loop().time()

        # Get processes before browser is started
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        options = ChromiumOptions()

        if self.headless:
            # Use --headless=new Chrome flag directly (recommended by pydoll docs)
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        if self.user_agent:
            options.add_argument(f"--user-agent={self.user_agent}")

        if self.proxy:
            proxy_server = f"{self.proxy['host']}:{self.proxy['port']}"
            protocol = self.proxy.get("protocol", "http")

            if "username" in self.proxy and "password" in self.proxy:
                options.add_argument(
                    f"--proxy-server={protocol}://{self.proxy['username']}:{self.proxy['password']}@{proxy_server}"
                )
            else:
                options.add_argument(f"--proxy-server={protocol}://{proxy_server}")

        try:
            # Initialize Chrome with custom options
            self.browser = Chrome(options=options)
            
            # Start browser and get the initial page/tab
            self.page = await asyncio.wait_for(
                self.browser.start(),
                timeout=settings.browser.action_timeout_s
            )
            logger.info(f"Pydoll browser started successfully: {self.name}")
        except Exception as e:
            logger.error(f"Failed to start Pydoll browser: {e}")
            raise

        # Track processes for resource usage
        process_children_after = parent_process.children(recursive=True)
        process_children_filtered = find_new_child_processes(process_children_before, process_children_after)
        self.process_list = process_children_filtered

    async def stop(self) -> None:
        """Stop the browser and clean up resources"""

        try:
            if self.browser:
                await asyncio.wait_for(self.browser.stop(),
                                       timeout=settings.browser.action_timeout_s)
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
            await asyncio.wait_for(
                self.page.go_to(url),
                timeout=settings.browser.page_load_timeout_s
            )
            success = True
        except Exception as e:
            logger.error(f"Pydoll failed navigation to {url}: {e}")
            success = False

        end_time = asyncio.get_event_loop().time()

        result: NavigationResult = {
            "url": url,
            "load_time": end_time - start_time,
            "success": success,
            "headers": {},  # Pydoll doesn't directly expose response headers in a simple property
        }

        return result

    async def reload_page(self) -> NavigationResult:
        """Reload the current page"""

        if not self.page:
            raise RuntimeError("Browser not started")

        start_time = asyncio.get_event_loop().time()

        try:
            await asyncio.wait_for(
                self.page.refresh(),
                timeout=settings.browser.page_load_timeout_s
            )
            success = True
        except Exception as e:
            logger.error(f"Pydoll failed to refresh page: {e}")
            success = False

        end_time = asyncio.get_event_loop().time()

        result: NavigationResult = {
            "url": await self.page.current_url,
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
        element_html = ""

        try:
            element = await asyncio.wait_for(
                self.page.query(css_selector, raise_exc=False),
                timeout=settings.browser.action_timeout_s
            )
            if element:
                element_found = True
                try:
                    # Evaluate innerHTML of the selector using page execution
                    inner_html_raw = await asyncio.wait_for(
                        self.page.execute_script(f"document.querySelector('{css_selector}').innerHTML"),
                        timeout=settings.browser.action_timeout_s
                    )
                    inner_html_result = self._extract_value_from_cdp(inner_html_raw)
                    if isinstance(inner_html_result, str) and inner_html_result:
                        element_html = inner_html_result
                    else:
                        text_raw = await asyncio.wait_for(
                            self.page.execute_script(f"document.querySelector('{css_selector}').textContent"),
                            timeout=settings.browser.action_timeout_s
                        )
                        text_result = self._extract_value_from_cdp(text_raw)
                        element_html = text_result if isinstance(text_result, str) else ""
                except Exception:
                    # Fallback to web element text extraction methods
                    try:
                        element_html = await element.get_element_text()
                    except Exception:
                        try:
                            element_html = await element.text
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
            return await asyncio.wait_for(
                self.page.page_source,
                timeout=settings.browser.action_timeout_s
            )
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
            # Wrap script in an IIFE
            wrapped_script = f"(() => {{\n{script}\n}})();"
            raw_result = await asyncio.wait_for(
                self.page.execute_script(wrapped_script),
                timeout=settings.browser.action_timeout_s
            )
            return self._extract_value_from_cdp(raw_result)
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

        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            await asyncio.wait_for(
                self.page.take_screenshot(path),
                timeout=settings.browser.action_timeout_s
            )
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
