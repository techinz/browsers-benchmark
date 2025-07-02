from typing import List, Dict, Callable

from pydantic import BaseModel, Field

from utils.targets.browser_data.creepjs import extract_creepjs_data
from utils.targets.browser_data.recaptcha_score import extract_recaptcha_score
from utils.targets.browser_data.twoip import extract_2ip_data
from utils.targets.check_bypass.amazon import check_amazon_bypass
from utils.targets.check_bypass.cloudflare_protected import check_cloudflare_bypass
from utils.targets.check_bypass.datadome_protected import check_datadome_bypass
from utils.targets.check_bypass.datadome_protected_2 import check_datadome2_bypass
from utils.targets.check_bypass.google_search import check_google_search_bypass
from utils.targets.check_bypass.ticketmaster import check_ticketmaster_bypass


class Target(BaseModel):
    """Configuration for a test target"""

    name: str = Field(..., description="Target name")
    url: str = Field(..., description="Target URL")
    check_function: str = Field(..., description="Function name to check the target")
    description: str = Field(default="", description="Target description")

    model_config = {"extra": "ignore"}


class BypassTargetsSettings(BaseModel):
    """Configuration for bypass targets"""

    targets: List[Target] = Field(
        default_factory=lambda: [
            Target(
                name="google_search",
                url="https://www.google.com/search?q=what+is+my+user+agent",
                check_function="check_google_search_bypass",
                description="Google Search bypass test"
            ),
            Target(
                name="cloudflare_protected",
                url="https://community.cloudflare.com",
                check_function="check_cloudflare_bypass",
                description="Cloudflare protection bypass test"
            ),
            Target(
                name="datadome_protected",
                url="https://datadome.co/customers-stories/",
                check_function="check_datadome_bypass",
                description="DataDome protection bypass test"
            ),
            Target(
                name="datadome_protected_2",
                url="https://www.hermes.com/",
                check_function="check_datadome2_bypass",
                description="DataDome protection bypass test (alternative)"
            ),
            Target(
                name="amazon_product",
                url="https://a.co/d/21FTKNR",
                check_function="check_amazon_bypass",
                description="Amazon captcha bypass test"
            ),
            Target(
                name="ticketmaster",
                url="https://www.ticketmaster.com/",
                check_function="check_ticketmaster_bypass",
                description="Ticketmaster (Imperva) bypass test"
            ),
        ]
    )

    checkers: Dict[str, Callable] = Field(
        default_factory=lambda: {
            "check_google_search_bypass": check_google_search_bypass,
            "check_cloudflare_bypass": check_cloudflare_bypass,
            "check_datadome_bypass": check_datadome_bypass,
            "check_datadome2_bypass": check_datadome2_bypass,
            "check_amazon_bypass": check_amazon_bypass,
            "check_ticketmaster_bypass": check_ticketmaster_bypass,
        }
    )

    model_config = {"extra": "ignore"}


class BrowserDataTargetsSettings(BaseModel):
    """Configuration for browser data extraction targets"""

    targets: List[Target] = Field(
        default_factory=lambda: [
            Target(
                name="recaptcha_score",
                url="https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
                check_function="extract_recaptcha_score",
                description="reCAPTCHA v3 score extraction"
            ),
            Target(
                name="creepjs",
                url="https://abrahamjuliot.github.io/creepjs/",
                check_function="extract_creepjs_data",
                description="CreepJS fingerprinting data extraction"
            ),
            Target(
                name="2ip",
                url="https://2ip.io/",
                check_function="extract_2ip_data",
                description="IP information extraction"
            )
        ]
    )

    checkers: Dict[str, Callable] = Field(
        default_factory=lambda: {
            "extract_recaptcha_score": extract_recaptcha_score,
            "extract_creepjs_data": extract_creepjs_data,
            "extract_2ip_data": extract_2ip_data
        }
    )

    model_config = {"extra": "ignore"}


class BenchmarkTargetsSettings(BaseModel):
    """Benchmark targets configuration"""

    bypass_targets: BypassTargetsSettings = Field(default_factory=BypassTargetsSettings)
    browser_data_targets: BrowserDataTargetsSettings = Field(default_factory=BrowserDataTargetsSettings)

    model_config = {"extra": "ignore"}


benchmark_targets_config = BenchmarkTargetsSettings()
