from typing import List

from utils.dataclasses import BypassTestResult


def calculate_metrics(
        bypass_results: List[BypassTestResult],
        memory_readings: List[int],
        cpu_readings: List[float]
) -> tuple[int, float, float]:
    """Calculate average metrics from test results"""
    
    avg_memory = int(sum(memory_readings) / len(memory_readings)) if memory_readings else 0
    avg_cpu = sum(cpu_readings) / len(cpu_readings) if cpu_readings else 0.0

    bypass_count = sum(1 for r in bypass_results if r.bypass and not r.error)
    bypass_rate = bypass_count / len(bypass_results) if bypass_results else 0.0

    return avg_memory, avg_cpu, bypass_rate
