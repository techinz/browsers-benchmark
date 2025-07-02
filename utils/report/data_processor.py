from typing import Dict, List, Any

import pandas as pd


def process_bypass_data(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Extract and process bypass data from benchmark results"""

    bypass_rows = []

    for engine_result in results:
        engine_name = engine_result["engine"]
        has_proxy = "proxy" in engine_name.lower()

        # base row with engine-level stats
        base_row = {
            "engine": engine_name,
            "has_proxy": has_proxy,
            "bypass_rate": engine_result["bypass_rate"],
            "avg_memory_mb": engine_result["average_memory_mb"],
            "avg_cpu_percent": engine_result["average_cpu_percent"],
        }

        # per-target stats
        for target in engine_result["bypass_targets_results"]:
            row = base_row.copy()
            row.update(target)
            bypass_rows.append(row)

    return pd.DataFrame(bypass_rows)


def process_browser_data(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Extract and process browser data from benchmark results"""

    browser_data_rows = []

    for engine_result in results:
        engine_name = engine_result["engine"]
        has_proxy = "proxy" in engine_name.lower()

        # base row with engine info
        base_row = {
            "engine": engine_name,
            "has_proxy": has_proxy,
        }

        # per-target metrics
        for target in engine_result["browser_data_targets_results"]:
            row = base_row.copy()
            row.update(target)
            browser_data_rows.append(row)

    return pd.DataFrame(browser_data_rows)
