from typing import List, Dict, Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from engines.nodriver.nodriver_engine import NoDriverEngine
from engines.nodriver.zendriver_engine import ZenDriverEngine
from engines.playwright.camoufox_engine import CamoufoxEngine
from engines.playwright.patchright_engine import PatchrightEngine
from engines.playwright.playwright_engine import PlaywrightEngine
from engines.playwright.tf_playwright_stealth_engine import TfPlaywrightStealthEngine
from engines.selenium.selenium_engine import SeleniumEngine
from engines.seleniumbase_engine import SeleniumBaseCDPEngine


class EngineConfig(BaseModel):
    """Configuration for a browser engine"""

    class_name: str = Field(..., description="Engine class name")
    params: Dict[str, Any] = Field(default_factory=dict, description="Engine parameters")

    model_config = {"extra": "ignore"}


class EnginesSettings(BaseSettings):
    """Configuration for all browser engines"""

    engines: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of engine configurations"
    )

    def __init__(self, **data):
        super().__init__(**data)
        self._initialize_engines()

    def _initialize_engines(self) -> None:
        """Initialize default engine configurations"""

        base_engines = [
            {
                "class": PlaywrightEngine,
                "params": {"headless": True, "name": "playwright-chrome_headless", "browser_type": "chromium"}
            },
            {
                "class": PlaywrightEngine,
                "params": {"headless": False, "name": "playwright-chrome", "browser_type": "chromium"}
            },
            {
                "class": PlaywrightEngine,
                "params": {"headless": True, "name": "playwright-firefox_headless", "browser_type": "firefox"}
            },
            {
                "class": PlaywrightEngine,
                "params": {"headless": False, "name": "playwright-firefox", "browser_type": "firefox"}
            },
            {
                "class": CamoufoxEngine,
                "params": {"headless": True, "name": "camoufox_headless"}
            },
            {
                "class": CamoufoxEngine,
                "params": {"headless": False, "name": "camoufox"}
            },
            {
                "class": TfPlaywrightStealthEngine,
                "params": {"headless": True, "name": "tf-playwright-stealth-chromium_headless",
                           "browser_type": "chromium"}
            },
            {
                "class": TfPlaywrightStealthEngine,
                "params": {"headless": False, "name": "tf-playwright-stealth-chromium", "browser_type": "chromium"}
            },
            {
                "class": TfPlaywrightStealthEngine,
                "params": {"headless": True, "name": "tf-playwright-stealth-firefox_headless",
                           "browser_type": "firefox"}
            },
            {
                "class": TfPlaywrightStealthEngine,
                "params": {"headless": False, "name": "tf-playwright-stealth-firefox", "browser_type": "firefox"}
            },
            {
                "class": PatchrightEngine,
                "params": {"headless": True, "name": "patchright_headless"}
            },
            {
                "class": PatchrightEngine,
                "params": {"headless": False, "name": "patchright"}
            },
            {
                "class": SeleniumEngine,
                "params": {"headless": True, "name": "selenium-chrome_headless__no_proxy", "browser_type": "chrome"}
            },
            {
                "class": SeleniumEngine,
                "params": {"headless": False, "name": "selenium-chrome__no_proxy", "browser_type": "chrome"}
            },
            {
                "class": ZenDriverEngine,
                "params": {"headless": True, "name": "zendriver-chrome_headless", "browser_type": "chrome"}
            },
            {
                "class": ZenDriverEngine,
                "params": {"headless": False, "name": "zendriver-chrome", "browser_type": "chrome"}
            },
            {
                "class": SeleniumBaseCDPEngine,
                "params": {"name": "seleniumbase-cdp-chrome"}
            },
        ]
        self.engines.extend(base_engines)

    model_config = {"extra": "ignore"}


engines_config = EnginesSettings()
