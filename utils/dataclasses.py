from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PerformanceMetrics:
    """Performance metrics for a single test run"""

    load_time_ms: int = 0
    memory_mb: int = 0
    cpu_percent: float = 0.0


@dataclass
class BypassTestResult:
    """Result of a bypass test"""

    target: str
    url: str
    bypass: bool = False
    error: Optional[str] = None
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)


@dataclass
class BrowserDataResult:
    """Result of browser data extraction"""

    target: str
    url: str
    error: Optional[str] = None
    # creepJS data
    creepjs_trust_score: Optional[float] = None
    creepjs_bot_score: Optional[float] = None
    creepjs_webrtc_ip: Optional[str] = None
    # recaptcha data
    recaptcha_score: Optional[float] = None
    # IP data
    ip: Optional[str] = None


@dataclass
class BenchmarkResults:
    """Complete benchmark results for an engine"""
    
    engine: str
    timestamp: str
    bypass_targets_results: List[BypassTestResult] = field(default_factory=list)
    browser_data_targets_results: List[BrowserDataResult] = field(default_factory=list)
    average_memory_mb: int = 0
    average_cpu_percent: float = 0.0
    bypass_rate: float = 0.0
    error: Optional[str] = None
