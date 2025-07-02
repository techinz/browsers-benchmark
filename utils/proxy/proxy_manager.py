import logging
import os
from typing import Dict, List, Optional
from urllib.parse import urlparse

from config.settings import settings

logger = logging.getLogger(__name__)


class ProxyManager:
    def __init__(self, proxies_file: str = settings.proxy.file_path):
        self.proxies_file = proxies_file
        self.available_proxies: List[str] = []
        self.used_proxies: List[str] = []
        self._load_proxies()

    def _load_proxies(self) -> None:
        """Load proxies from file"""

        try:
            if os.path.exists(self.proxies_file):
                with open(self.proxies_file, 'r', encoding='utf-8') as f:
                    proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    self.available_proxies = proxies.copy()
                    logger.info(f"Loaded {len(self.available_proxies)} proxies from {self.proxies_file}")
            else:
                logger.warning(f"Proxies file {self.proxies_file} not found")
                self.available_proxies = []
        except Exception as e:
            logger.error(f"Failed to load proxies from {self.proxies_file}: {e}")
            self.available_proxies = []

    def get_proxy(self) -> Optional[Dict[str, str]]:
        """Get next available proxy and mark it as used"""

        if not self.available_proxies:
            logger.error("No more available proxies")
            return None

        proxy_url = self.available_proxies.pop(0)
        self.used_proxies.append(proxy_url)

        try:
            parsed = urlparse(proxy_url)
            proxy_config = {
                "protocol": parsed.scheme,
                "host": parsed.hostname,
                "port": str(parsed.port) if parsed.port else "8080",
            }

            if parsed.username and parsed.password:
                proxy_config["username"] = parsed.username
                proxy_config["password"] = parsed.password

            logger.info(f"Assigned proxy {parsed.hostname}:{parsed.port} ({len(self.available_proxies)} remaining)")
            return proxy_config
        except Exception as e:
            logger.error(f"Failed to parse proxy URL {proxy_url}: {e}")
            return None

    def get_fallback_proxy(self) -> Optional[Dict[str, str]]:
        """Get another proxy if current one fails"""
        return self.get_proxy()

    def has_available_proxies(self) -> bool:
        """Check if there are still available proxies"""
        return len(self.available_proxies) > 0

    def get_available_count(self) -> int:
        """Get number of available proxies"""
        return len(self.available_proxies)

    def validate_proxy_count(self, required_count: int) -> bool:
        """Validate if we have enough proxies for the required engines"""

        total_proxies = len(self.available_proxies) + len(self.used_proxies)
        if total_proxies != required_count:
            logger.error(
                f"Wrong count of proxies available. Required: {required_count}, "
                f"Available: {total_proxies} (in {self.proxies_file})"
            )
            return False
        return True

    def reset(self) -> None:
        """Reset proxy manager - move all used proxies back to available"""

        self.available_proxies.extend(self.used_proxies)
        self.used_proxies = []
        logger.info(f"Reset proxy manager. {len(self.available_proxies)} proxies available")


proxy_manager = ProxyManager()
