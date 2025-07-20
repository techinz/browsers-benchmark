import json
import os

from config.settings import settings
from utils.dataclasses import BenchmarkResults


def create_directory_structure(timestamp: str) -> tuple[str, str, str]:
    """
    Create the necessary directory structure for results

    :param timestamp: Timestamp to create unique directory names
    :return: Tuple containing paths to result directory, media directory, and screenshots directory
    """

    result_path = os.path.join(settings.paths.results_path, timestamp)
    media_path = os.path.join(result_path, settings.paths.media_dir)
    screenshots_path = os.path.join(media_path, settings.paths.screenshots_dir)

    directories = [
        settings.paths.results_path,
        result_path,
        media_path,
        screenshots_path,
        settings.paths.binaries_path,
        settings.paths.profiles_path
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    return result_path, media_path, screenshots_path


def save_results(results: BenchmarkResults, result_path: str) -> str:
    """
    Save benchmark results to JSON file (appending to existing results if file already exists)

    :param results: BenchmarkResults dataclass containing the benchmark data
    :param result_path: Path to save the results file
    """

    results_file = os.path.join(result_path, f"benchmark_results.json")

    # Convert dataclasses to dict for JSON serialization
    results_dict = {
        "engine": results.engine,
        "timestamp": results.timestamp,
        "bypass_targets_results": [
            {
                "target": r.target,
                "url": r.url,
                "bypass": r.bypass,
                "error": r.error,
                "load_time_ms": r.performance.load_time_ms,
                "memory_mb": r.performance.memory_mb,
                "cpu_percent": r.performance.cpu_percent
            } for r in results.bypass_targets_results
        ],
        "browser_data_targets_results": [
            {
                "target": r.target,
                "url": r.url,
                "error": r.error,
                "creepjs_trust_score": r.creepjs_trust_score,
                "creepjs_bot_score": r.creepjs_bot_score,
                "creepjs_webrtc_ip": r.creepjs_webrtc_ip,
                "recaptcha_score": r.recaptcha_score,
                "ip": r.ip
            } for r in results.browser_data_targets_results
        ],
        "average_memory_mb": results.average_memory_mb,
        "average_cpu_percent": results.average_cpu_percent,
        "bypass_rate": results.bypass_rate,
        "error": results.error
    }

    existing_results = []
    if os.path.exists(results_file):
        try:
            with open(results_file, "r") as f:
                existing_results = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_results = []

    # delete old results for this engine if they exist
    existing_results = [r for r in existing_results if r.get("engine") != results.engine]

    all_results = existing_results + [results_dict]

    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=2)

    return results_file
