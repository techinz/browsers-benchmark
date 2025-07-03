import asyncio
import logging
import os
from typing import Dict, Optional, Any, Tuple

import psutil
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from engines.base import BrowserEngine, NavigationResult
from utils.process import find_new_child_processes

logger = logging.getLogger(__name__)

"""
This Selenium Browser Engine implementation doesn't support proxies with auth.
It is possible to add it, but that requires a lot of additional setup and I think no one even needs it 
since Selenium is deprecated. It is easier to do with selenium-wire, which is also deprecated.
"""


class SeleniumBase(BrowserEngine):
    def __init__(
            self,
            name: str = "selenium-chrome__no_proxy",
            browser_type: str = "chrome",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        super().__init__(name, proxy)
        self.browser_type = browser_type  # chrome, firefox
        self.headless = headless
        self.user_agent = user_agent

        self.driver = None
        self.wait = None

    @property
    def supported_proxy_protocols(self) -> list[str]:
        """Selenium doesn't support proxies with auth, so we consider it as no proxy protocols because no one uses it anyway"""
        return []

    async def start(self) -> None:
        """Initialize and start the browser"""

        self._start_time = asyncio.get_event_loop().time()

        # get processes before browser is started
        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        # configure browser options
        options = self._get_browser_options()

        if self.headless:
            options.add_argument("--headless")

        if self.user_agent:
            options.add_argument(f"--user-agent={self.user_agent}")

        # add common arguments for better stealthiness
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # only add experimental options for chrome
        if self.browser_type.lower() == "chrome" and isinstance(options, ChromeOptions):
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

        # initialize driver
        self.driver = self._create_driver(options)

        # set up wait object for explicit waits
        self.wait = WebDriverWait(self.driver, settings.browser.page_load_timeout_s)

        # remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # track process for resource usage
        process_children_after = parent_process.children(recursive=True)
        process_children_filtered = find_new_child_processes(process_children_before, process_children_after)
        self.process_list = process_children_filtered

    def _get_browser_options(self):
        """Get browser-specific options object"""

        if self.browser_type.lower() == "chrome":
            return ChromeOptions()
        elif self.browser_type.lower() == "firefox":
            return FirefoxOptions()
        elif self.browser_type.lower() == "edge":
            return EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

    def _create_driver(self, options):
        """Create WebDriver instance based on browser type"""

        if self.browser_type.lower() == "chrome":
            return webdriver.Chrome(options=options)
        elif self.browser_type.lower() == "firefox":
            return webdriver.Firefox(options=options)
        elif self.browser_type.lower() == "edge":
            return webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

    async def stop(self) -> None:
        """Stop the browser and clean up resources"""

        try:
            if self.driver:
                self.driver.quit()
        except Exception:
            pass
        self.driver = None
        self.wait = None
        self.process_list = None

    async def navigate(self, url: str) -> NavigationResult:
        """Navigate to url and return page data"""

        if not self.driver:
            raise RuntimeError("Browser not started")

        start_time = asyncio.get_event_loop().time()

        try:
            self.driver.get(url)
            success = True
        except WebDriverException as e:
            success = False

        end_time = asyncio.get_event_loop().time()

        result: NavigationResult = {
            "url": url,
            "load_time": end_time - start_time,
            "success": success,
            "headers": {},  # selenium doesn't provide response headers
        }

        return result

    async def reload_page(self) -> NavigationResult:
        """Reload the current page"""

        if not self.driver:
            raise RuntimeError("Browser not started")

        start_time = asyncio.get_event_loop().time()

        try:
            self.driver.refresh()
            success = True
        except WebDriverException:
            success = False

        end_time = asyncio.get_event_loop().time()

        result: NavigationResult = {
            "url": self.driver.current_url if self.driver else "",
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

        if not self.driver:
            raise RuntimeError("Browser not started")

        element_found = False
        element_html = ''

        try:
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            if element:
                element_found = True
                element_html = element.get_attribute('innerHTML') or element.text
        except Exception:
            pass

        return element_found, element_html

    async def get_page_content(self) -> str:
        """Get current page html content"""

        if not self.driver:
            raise RuntimeError("Browser not started")

        return self.driver.page_source

    async def execute_js(self, script: str) -> Any:
        """Execute javascript in browser context"""

        if not self.driver:
            raise RuntimeError("Browser not started")

        return self.driver.execute_script(script)

    async def screenshot(self, path: str) -> None:
        """Take a screenshot of the current page"""

        if not self.driver:
            raise RuntimeError("Browser not started")

        # ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)

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
