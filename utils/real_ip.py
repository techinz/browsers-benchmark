import json
import logging
import re
from typing import Optional
from urllib.request import ProxyHandler, build_opener

logger = logging.getLogger(__name__)

REAL_IP_PLACEHOLDER = "REAL_IP"

_real_ip: Optional[str] = None


def detect_real_ip() -> Optional[str]:
    """Look up this machine's public IP (direct request, bypassing any proxy) so it can be masked in results"""

    global _real_ip
    try:
        # empty ProxyHandler: ignore HTTP(S)_PROXY env vars, we need the machine's own IP
        opener = build_opener(ProxyHandler({}))
        with opener.open("https://api.ipify.org?format=json", timeout=15) as resp:
            _real_ip = json.loads(resp.read())["ip"]
        logger.info(f"Real IP detected, it will be saved as {REAL_IP_PLACEHOLDER} in results and screenshots")
    except Exception as e:
        _real_ip = None
        logger.warning(f"Failed to detect the real IP, it won't be masked in results and screenshots: {e}")
    return _real_ip


def get_real_ip() -> Optional[str]:
    return _real_ip


def _real_ip_pattern() -> str:
    """Regex for the real IP, also when written with dashes or underscores (e.g. in reverse DNS host names)"""

    if ":" in _real_ip:
        return re.escape(_real_ip)
    return r"[.\-_]".join(_real_ip.split("."))


def mask_real_ip(text: str) -> str:
    """Replace the real IP in text with the placeholder"""

    if not _real_ip:
        return text
    return re.sub(rf"(?<![\d.]){_real_ip_pattern()}(?!\d|\.\d)", REAL_IP_PLACEHOLDER, text)


def mask_real_ip_js() -> Optional[str]:
    """JS that replaces the real IP in the page's visible text (incl. open shadow roots) before a screenshot"""

    if not _real_ip:
        return None
    return (
        f"const re = new RegExp('(^|[^\\\\d.])' + {json.dumps(_real_ip_pattern())} + '(?!\\\\d|\\\\.\\\\d)', 'g');\n"
        "const mask = (value) => value.replace(re, '$1" + REAL_IP_PLACEHOLDER + "');\n"
        "const walk = (root) => {\n"
        "  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);\n"
        "  let n;\n"
        "  while ((n = w.nextNode())) {\n"
        "    if (n.nodeType === Node.TEXT_NODE) {\n"
        "      const masked = mask(n.nodeValue);\n"
        "      if (masked !== n.nodeValue) n.nodeValue = masked;\n"
        "    } else {\n"
        "      if (n.shadowRoot) walk(n.shadowRoot);\n"
        "      if ('value' in n && typeof n.value === 'string' && mask(n.value) !== n.value) n.value = mask(n.value);\n"
        "    }\n"
        "  }\n"
        "};\n"
        "walk(document.documentElement);\n"
        "return true;"
    )
