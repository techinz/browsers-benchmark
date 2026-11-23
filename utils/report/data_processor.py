from typing import Dict, List, Any

import pandas as pd


def process_bypass_data(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Extract and process bypass data from benchmark results

    :param results: List of benchmark results for each engine
    :return: DataFrame containing bypass rates and engine stats
    """

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
    """
    Extract and process browser data from benchmark results

    :param results: List of browser data results for each engine
    :return: DataFrame containing browser data metrics and engine stats
    """

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


def process_detection_data(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Extract bot detection test verdicts from benchmark results

    :param results: List of benchmark results for each engine
    :return: DataFrame with one row per engine and detection test
    """

    detection_rows = []

    for engine_result in results:
        for test in engine_result.get("detection_targets_results", []):
            detection_rows.append({
                "engine": engine_result["engine"],
                "target": test["target"],
                "verdict": test.get("verdict") if not test.get("error") else None,
                "summary": test.get("summary"),
                "risk": test.get("risk") if not test.get("error") else None,
                "error": test.get("error"),
            })

    return pd.DataFrame(detection_rows, columns=["engine", "target", "verdict", "summary", "risk", "error"])


def summarize_detection(detection_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize bot detection results per engine

    :param detection_df: DataFrame from process_detection_data
    :return: DataFrame indexed by engine with detected/suspicious/total (finished tests)/errors counts and
        risk (average detection risk 0-100 over the finished tests), least detectable engines first
    """

    if detection_df.empty:
        return pd.DataFrame(columns=["detected", "suspicious", "total", "errors", "risk"])

    summary = detection_df.groupby("engine").agg(
        detected=("verdict", lambda v: int((v == "bot").sum())),
        suspicious=("verdict", lambda v: int((v == "suspicious").sum())),
        total=("verdict", lambda v: int(v.notna().sum())),
        errors=("verdict", lambda v: int(v.isna().sum())),
        risk=("risk", lambda r: float(pd.to_numeric(r, errors="coerce").mean())),
    )
    return summary.sort_index().sort_values(["risk", "detected", "errors"], kind="stable")
