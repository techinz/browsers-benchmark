import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ProxySettings(BaseModel):
    """Configuration settings for the proxy"""

    enabled: bool = True
    file_path: str = "documents/proxies.txt"
    max_retries: int = 3  # maximum number of proxy fallback attempts

    model_config = {"extra": "ignore"}


class PathSettings(BaseModel):
    """Configuration settings for file paths"""

    documents_path: str = "documents"
    binaries_dir: str = "binaries"
    profiles_dir: str = "profiles"
    results_path: str = "results"
    media_dir: str = "media"
    screenshots_dir: str = "screenshots"

    @property
    def binaries_path(self) -> str:
        return os.path.join(self.documents_path, self.binaries_dir)

    @property
    def profiles_path(self) -> str:
        return os.path.join(self.documents_path, self.profiles_dir)

    model_config = {"extra": "ignore"}


class BrowserSettings(BaseModel):
    """Configuration settings for browser engines"""

    action_timeout_s: int = 60  # maximum time to wait for actions like search of elements, screenshots, clicks, etc.
    page_load_timeout_s: int = 60  # maximum time to wait for page load in seconds
    page_stabilization_delay_s: int = 5  # time to wait for page stabilization after navigation
    headless: bool = True

    model_config = {"extra": "ignore"}


class Settings(BaseSettings):
    """Main application settings"""

    # proxy
    PROXY_ENABLED: bool = True
    PROXY_FILE_PATH: str = "documents/proxies.txt"
    PROXY_MAX_RETRIES: int = 3

    # browser
    ACTION_TIMEOUT_S: int = 30  # maximum time to wait for actions like search of elements, screenshots, clicks, etc.
    PAGE_LOAD_TIMEOUT_S: int = 90  # maximum time to wait for page load in seconds
    PAGE_STABILIZATION_DELAY_S: int = 5  # time to wait for page stabilization after navigation
    BROWSER_HEADLESS: bool = True  # run browser in headless mode

    # paths
    DOCUMENTS_PATH: str = "documents"
    BINARIES_DIR: str = "binaries"
    PROFILES_DIR: str = "profiles"
    RESULTS_PATH: str = "results"
    MEDIA_DIR: str = "media"
    SCREENSHOTS_DIR: str = "screenshots"

    # constants
    MAX_RETRIES: int = 3  # maximum retries for failed tests

    @property
    def proxy(self) -> ProxySettings:
        """Get proxy configuration"""
        return ProxySettings(
            enabled=self.PROXY_ENABLED,
            file_path=self.PROXY_FILE_PATH,
            max_retries=self.PROXY_MAX_RETRIES
        )

    @property
    def paths(self) -> PathSettings:
        """Get path configuration"""
        return PathSettings(
            documents_path=self.DOCUMENTS_PATH,
            binaries_dir=self.BINARIES_DIR,
            profiles_dir=self.PROFILES_DIR,
            results_path=self.RESULTS_PATH,
            media_dir=self.MEDIA_DIR,
            screenshots_dir=self.SCREENSHOTS_DIR
        )

    @property
    def browser(self) -> BrowserSettings:
        """Get browser configuration"""
        return BrowserSettings(
            action_timeout_s=self.ACTION_TIMEOUT_S,
            page_load_timeout_s=self.PAGE_LOAD_TIMEOUT_S,
            page_stabilization_delay_s=self.PAGE_STABILIZATION_DELAY_S,
            headless=self.BROWSER_HEADLESS
        )

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore",
    }


settings = Settings()
