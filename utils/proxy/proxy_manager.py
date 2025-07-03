import logging
import os
from collections.abc import Callable
from typing import Dict, List, Optional, Set, Any, Tuple
from urllib.parse import urlparse

from config.settings import settings

logger = logging.getLogger(__name__)


def is_proxy_related_error(error: Exception) -> bool:
    """
    Determine if an error is proxy-related and warrants a proxy fallback

    :param error: Exception object to check

    :return: True for proxy/network errors, False for other errors
    """

    error_str = str(error).lower()
    error_type = type(error).__name__.lower()

    # proxy-related error patterns
    proxy_error_patterns = [
        # connection issues
        "connection", "connect", "refused", "timeout", "timed out",
        # proxy-specific errors
        "proxy", "authentication", "unauthorized", "407",
        "err_proxy_connection_failed", "proxy_connection_failed",
        # network issues
        "network", "dns", "resolve", "unreachable",
        # playwright-specific network errors
        "net::", "err_", "failed to navigate", "navigation timeout",
        "err_timed_out", "err_connection_refused", "err_network_changed",
        # selenium-specific errors
        "webdriver", "selenium", "chrome not reachable", "firefox not responding",
        "session not created", "unknown error", "chrome failed to start",
        # HTTP errors that might indicate proxy issues
        "502", "503", "504", "bad gateway", "service unavailable", "gateway timeout"
    ]

    # playwright-specific error types that are often proxy-related
    network_error_types = [
        "timeouterror", "networkerror", "browsererror",
        # selenium error types
        "webdriverexception", "sessionnotcreatedexception", "timeoutexception"
    ]

    # check if error message contains proxy-related keywords
    for pattern in proxy_error_patterns:
        if pattern in error_str:
            logger.debug(f"Identified proxy-related error pattern: '{pattern}' in '{error_str}'")
            return True

    # check if error type is network-related
    if error_type in network_error_types:
        logger.debug(f"Identified proxy-related error type: '{error_type}'")
        return True

    # check for specific error types
    if "timeout" in error_type or "connection" in error_type:
        logger.debug(f"Identified proxy-related error type: '{error_type}'")
        return True

    logger.debug(f"Error not identified as proxy-related: {error_type} - {error_str}")
    return False


class ProxyManager:
    def __init__(self, proxies_file: str = settings.proxy.file_path):
        self.proxies_file = proxies_file
        self.available_proxies: List[str] = []
        self.used_proxies: List[str] = []
        self.failed_proxies: Set[str] = set()  # track proxies that failed
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
                "url": proxy_url  # store original url for tracking
            }

            if parsed.username and parsed.password:
                proxy_config["username"] = parsed.username
                proxy_config["password"] = parsed.password

            logger.info(f"Assigned proxy {proxy_url} ({len(self.available_proxies)} remaining)")
            return proxy_config
        except Exception as e:
            logger.error(f"Failed to parse proxy URL {proxy_url}: {e}")
            return None

    def mark_proxy_failed(self, proxy: Dict[str, str]) -> None:
        """Mark a proxy as failed"""

        proxy_url = proxy.get("url")
        if proxy_url:
            self.failed_proxies.add(proxy_url)
            logger.warning(f"Marked proxy {proxy_url} as failed")

    def get_fallback_proxy(self, failed_proxy: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        """Get another proxy if current one fails"""

        if failed_proxy:
            self.mark_proxy_failed(failed_proxy)

        # filter out failed proxies from available ones
        original_count = len(self.available_proxies)
        self.available_proxies = [p for p in self.available_proxies if p not in self.failed_proxies]
        filtered_count = original_count - len(self.available_proxies)

        if filtered_count > 0:
            logger.info(f"Filtered out {filtered_count} failed proxies, {len(self.available_proxies)} remain available")

        return self.get_proxy()

    def get_proxy_by_protocol(self, supported_protocols: List[str]) -> Optional[Dict[str, str]]:
        """Get next available proxy that matches one of the supported protocols"""

        if not self.available_proxies:
            logger.error("No more available proxies")
            return None

        # filter proxies by supported protocols
        compatible_proxies = []
        for proxy_url in self.available_proxies:
            try:
                parsed = urlparse(proxy_url)
                if parsed.scheme in supported_protocols:
                    compatible_proxies.append(proxy_url)
            except Exception as e:
                logger.error(f"Failed to parse proxy URL {proxy_url}: {e}")
                continue

        if not compatible_proxies:
            logger.error(f"No proxies found with supported protocols {supported_protocols}")
            return None

        # use first compatible proxy
        proxy_url = compatible_proxies[0]
        self.available_proxies.remove(proxy_url)
        self.used_proxies.append(proxy_url)

        try:
            parsed = urlparse(proxy_url)
            proxy_config = {
                "protocol": parsed.scheme,
                "host": parsed.hostname,
                "port": str(parsed.port) if parsed.port else "8080",
                "url": proxy_url  # store original url for tracking
            }

            if parsed.username and parsed.password:
                proxy_config["username"] = parsed.username
                proxy_config["password"] = parsed.password

            logger.info(
                f"Assigned proxy {proxy_url} with protocol {parsed.scheme} ({len(self.available_proxies)} remaining)")
            return proxy_config
        except Exception as e:
            logger.error(f"Failed to parse proxy URL {proxy_url}: {e}")
            return None

    def get_fallback_proxy_by_protocol(self, supported_protocols: List[str],
                                       failed_proxy: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        """Get another proxy with supported protocol if current one fails"""

        if failed_proxy:
            self.mark_proxy_failed(failed_proxy)

        # filter out failed proxies from available ones
        original_count = len(self.available_proxies)
        self.available_proxies = [p for p in self.available_proxies if p not in self.failed_proxies]
        filtered_count = original_count - len(self.available_proxies)

        if filtered_count > 0:
            logger.info(f"Filtered out {filtered_count} failed proxies, {len(self.available_proxies)} remain available")

        return self.get_proxy_by_protocol(supported_protocols)

    def has_available_proxies(self) -> bool:
        """Check if there are still available proxies (excluding failed ones)"""

        available_non_failed = [p for p in self.available_proxies if p not in self.failed_proxies]
        return len(available_non_failed) > 0

    def get_available_count(self) -> int:
        """Get number of available proxies (excluding failed ones)"""

        available_non_failed = [p for p in self.available_proxies if p not in self.failed_proxies]
        return len(available_non_failed)

    def get_failed_count(self) -> int:
        """Get number of failed proxies"""

        return len(self.failed_proxies)

    def validate_proxy_count(self, required_count: int) -> bool:
        """Validate if we have enough proxies for the required engines"""

        total_proxies = len(self.available_proxies) + len(self.used_proxies)
        if total_proxies < required_count:
            logger.error(
                f"Not enough proxies available. Required: {required_count}, "
                f"Available: {total_proxies} (in {self.proxies_file})"
            )
            return False
        return True

    def validate_proxy_count_by_protocol(self, engines_with_protocols: List[Tuple[str, List[str]]]) -> bool:
        """Validate if we have enough compatible proxies for engines with their supported protocols"""

        # count available proxies by protocol
        protocol_availability = {}
        for proxy_url in self.available_proxies + self.used_proxies:
            try:
                parsed = urlparse(proxy_url)
                protocol = parsed.scheme
                if protocol not in protocol_availability:
                    protocol_availability[protocol] = 0
                protocol_availability[protocol] += 1
            except Exception:
                continue

        # check which engines can be satisfied and which cannot
        satisfied_engines = []
        unsatisfied_engines = []

        for engine_name, supported_protocols in engines_with_protocols:
            # check if any of the supported protocols has available proxies
            has_compatible_proxy = False

            for protocol in supported_protocols:
                if protocol_availability.get(protocol, 0) > 0:
                    has_compatible_proxy = True
                    break

            if not supported_protocols:
                has_compatible_proxy = True

            if has_compatible_proxy:
                satisfied_engines.append(f"{engine_name} (supports: {', '.join(supported_protocols)})")
            else:
                unsatisfied_engines.append(f"{engine_name} (supports: {', '.join(supported_protocols)})")

        if unsatisfied_engines:
            logger.error("The following engines don't have compatible proxies:")
            for engine in unsatisfied_engines:
                logger.error(f"\t{engine}")

            logger.info(f"Available proxy protocols: {protocol_availability}")
            return False

        logger.info("All engines have compatible proxies:")
        for engine in satisfied_engines:
            logger.info(f"  {engine}")
        logger.info(f"Available proxy protocols: {protocol_availability}")
        return True

    def reset(self) -> None:
        """Reset proxy manager - move all used proxies back to available"""

        self.available_proxies.extend(self.used_proxies)
        self.used_proxies = []
        # don't reset failed proxies - they remain failed for the session
        logger.info(
            f"Reset proxy manager. {len(self.available_proxies)} proxies available ({len(self.failed_proxies)} marked as failed)")

    def get_stats(self) -> Dict[str, int]:
        """Get proxy usage statistics"""

        return {
            "total_loaded": len(self.available_proxies) + len(self.used_proxies) + len(self.failed_proxies),
            "available": len(self.available_proxies),
            "used": len(self.used_proxies),
            "failed": len(self.failed_proxies)
        }


async def handle_proxy_fallback(engine, target_name: str, original_error: Exception, retry_function: Callable,
                                proxy_manager_instance=None) -> Tuple[Any, Optional[str]]:
    """
    Handle proxy fallback when a proxy-related error occurs.
    
    :param engine: The browser engine instance
    :param target_name: Name of the target being tested
    :param original_error: The original error that occurred
    :param retry_function: The async function to retry (should be a coroutine)
    :param proxy_manager_instance: ProxyManager instance
        
    :return: tuple: (result, error_message) where result is the retry result or None,
        and error_message is the error string if failed or None if successful
    """

    if proxy_manager_instance is None:
        proxy_manager_instance = proxy_manager

    logger.warning(f"Proxy-related error for {target_name}: {original_error}")

    # try to get a fallback proxy and restart the engine
    current_proxy = getattr(engine, 'proxy', None)
    if not (current_proxy and proxy_manager_instance.has_available_proxies()):
        logger.error(f"Proxy fallback not available for {target_name}")
        return None, str(original_error)

    # get supported protocols from engine and use protocol-aware fallback
    supported_protocols = getattr(engine, 'supported_proxy_protocols', ['http', 'https'])
    fallback_proxy = proxy_manager_instance.get_fallback_proxy_by_protocol(supported_protocols, current_proxy)
    if not fallback_proxy:
        logger.error(f"No compatible fallback proxy available for {target_name} (supports: {supported_protocols})")
        return None, str(original_error)

    logger.info(
        f"Retrying {target_name} with fallback {fallback_proxy['protocol']} proxy {fallback_proxy.get('host')}:{fallback_proxy.get('port')}")

    try:
        # stop current engine
        await engine.stop()

        # update engine proxy
        engine.proxy = fallback_proxy

        # restart engine with new proxy
        await engine.start()

        # retry the operation
        result = await retry_function()
        logger.info(f"Fallback proxy successful for {target_name}")
        return result, None
    except Exception as fallback_error:
        logger.error(f"Fallback proxy also failed for {target_name}: {fallback_error}")
        return None, f"Original: {str(original_error)}, Fallback: {str(fallback_error)}"


proxy_manager = ProxyManager()
