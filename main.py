import asyncio
import gc
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

from config.benchmark_targets import benchmark_targets_config
from config.engines import engines_config
from config.settings import settings
from engines.base import BrowserEngine
from utils.dataclasses import BypassTestResult, BrowserDataResult, BenchmarkResults
from utils.io import create_directory_structure, save_results
from utils.logging.logging import setup_logging
from utils.metrics import calculate_metrics
from utils.proxy.proxy_manager import proxy_manager
from utils.report import generate_report
from utils.retry import retry_with_backoff
from utils.screenshot import take_screenshot

setup_logging()

logger = logging.getLogger(__name__)


async def test_bypass_target(
        engine: BrowserEngine,
        target: Dict[str, Any],
        screenshots_path: str
) -> BypassTestResult:
    """Test a single bypass target"""

    logger.info(f"Testing {engine.name} against {target['name']}...")

    result = BypassTestResult(target=target["name"], url=target["url"])

    async def attempt_bypass_test():
        navigation_result = await engine.navigate(target["url"])
        result.performance.load_time_ms = int(navigation_result.get("load_time", 0) * 1000)

        await asyncio.sleep(settings.browser.page_stabilization_delay_s)  # wait for page to stabilize

        result.performance.memory_mb = int(engine.get_memory_usage())
        result.performance.cpu_percent = engine.get_cpu_usage()

        check_function = benchmark_targets_config.bypass_targets.checkers.get(target["check_function"])
        if check_function is None:
            raise ValueError(f"Check function '{target['check_function']}' not found")

        result.bypass = await check_function(engine)
        return result

    try:
        result = await retry_with_backoff(attempt_bypass_test)
    except Exception as e:
        result.error = str(e)
        logger.warning(f'{engine.name} failed bypass test for {target["name"]}: {e}')

    await take_screenshot(engine, screenshots_path, target["name"])

    return result


async def extract_browser_data(
        engine: BrowserEngine,
        target: Dict[str, Any],
        screenshots_path: str
) -> BrowserDataResult:
    """Extract browser data from a target"""

    logger.info(f"Extracting browser data from {target['name']} using {engine.name}...")

    result = BrowserDataResult(target=target["name"], url=target["url"])

    async def attempt_data_extraction():
        await engine.navigate(target["url"])
        await asyncio.sleep(settings.browser.page_stabilization_delay_s)  # ensure page is fully loaded

        extract_function = benchmark_targets_config.browser_data_targets.checkers.get(target["check_function"])
        if extract_function is None:
            raise ValueError(f"Extract function '{target['check_function']}' not found")

        target_data = await extract_function(engine)

        # update result with extracted data
        for key, value in target_data.items():
            if hasattr(result, key):
                setattr(result, key, value)

        return result

    try:
        result = await retry_with_backoff(attempt_data_extraction)
    except Exception as e:
        result.error = str(e)
        logger.warning(f'{engine.name} failed data extraction for {target["name"]}: {e}')

    await take_screenshot(engine, screenshots_path, target["name"])

    return result


async def run_benchmark_for_engine(
        engine_cls,
        engine_params: Dict[str, Any],
        bypass_targets: List[Dict[str, Any]],
        browser_data_targets: List[Dict[str, Any]],
        screenshots_path: str,
        proxy: Optional[Dict[str, str]] = None
) -> BenchmarkResults | None:
    """Run benchmark for a browser engine"""

    if proxy:
        engine_params = {**engine_params, "proxy": proxy}

    engine = engine_cls(**engine_params)
    engine_screenshots_path = os.path.join(screenshots_path, engine.name)
    os.makedirs(engine_screenshots_path, exist_ok=True)

    results = BenchmarkResults(
        engine=engine.name,
        timestamp=datetime.now().isoformat()
    )

    memory_readings: List[int] = []
    cpu_readings: List[float] = []

    try:
        await engine.start()
        logger.info(f"Started {engine.name} engine")

        # test bypass targets
        for target in bypass_targets:
            bypass_result = await test_bypass_target(engine, target, engine_screenshots_path)
            results.bypass_targets_results.append(bypass_result)

            if not bypass_result.error:
                memory_readings.append(bypass_result.performance.memory_mb)
                cpu_readings.append(bypass_result.performance.cpu_percent)

            await asyncio.sleep(1)

        # extract browser data
        for target in browser_data_targets:
            data_result = await extract_browser_data(engine, target, engine_screenshots_path)
            results.browser_data_targets_results.append(data_result)
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Critical error during benchmark for {engine.name}: {e}")
        results.error = str(e)
    finally:
        # calculate final metrics
        avg_memory, avg_cpu, bypass_rate = calculate_metrics(
            results.bypass_targets_results, memory_readings, cpu_readings
        )
        results.average_memory_mb = avg_memory
        results.average_cpu_percent = avg_cpu
        results.bypass_rate = bypass_rate

        # cleanup
        try:
            await engine.stop()
            logger.info(f"Stopped {engine.name} engine")
        except Exception as e:
            logger.error(f"Error stopping engine {engine.name}: {e}")

    return results


async def run_all_benchmarks() -> None:
    """Run benchmarks for all configured engines"""

    # validate proxy setup before starting
    if not settings.proxy.enabled:
        logger.warning("⚠️ PROXIES ARE DISABLED! Results may be inaccurate due to IP reputation.")
        logger.warning("\tEnable proxies in .env for reliable benchmark results.")
        return

    # check if we have enough proxies for all engines (one per engine)
    engine_count = len(engines_config.engines)
    if not proxy_manager.validate_proxy_count(engine_count):
        raise ValueError(
            f"Wrong proxy count! Need {engine_count} proxies but "
            f"{proxy_manager.get_available_count()} available in {settings.proxy.file_path}"
        )

    logger.info(f"Proxy validation passed: {proxy_manager.get_available_count()} proxies available for {engine_count} engines")

    timestamp = datetime.now().strftime("%Y.%m.%d__%H_%M_%S")
    result_path, media_path, screenshots_path = create_directory_structure(timestamp)

    try:
        all_results: List[BenchmarkResults] = []

        if not engines_config.engines:
            logger.error("No engines configured for benchmarking")
            return

        # test each engine
        for engine_config in engines_config.engines:
            engine_name = engine_config['params']['name']
            logger.info(f"\n===== Testing {engine_name} =====")

            # get proxy for this engine if enabled
            proxy = None
            if settings.proxy.enabled:
                proxy = proxy_manager.get_proxy()
                if not proxy:
                    logger.error(f"No proxy available for {engine_name}, skipping...")
                    continue

            try:
                results = await run_benchmark_for_engine(
                    engine_cls=engine_config["class"],
                    engine_params=engine_config["params"],
                    bypass_targets=[target.model_dump() for target in benchmark_targets_config.bypass_targets.targets],
                    browser_data_targets=[target.model_dump() for target in
                                          benchmark_targets_config.browser_data_targets.targets],
                    screenshots_path=screenshots_path,
                    proxy=proxy,
                )
                all_results.append(results)
            except Exception as e:
                logger.error(f"Failed to run benchmark for {engine_name}: {e}")

                error_result = BenchmarkResults(
                    engine=engine_name,
                    timestamp=datetime.now().isoformat(),
                    error=str(e)
                )
                all_results.append(error_result)

        # save and report results
        benchmark_results_path = save_results(all_results, result_path)
        logger.info(f"\nBenchmark complete. Results saved to {benchmark_results_path}")

        # generate report
        try:
            generate_report(benchmark_results_path, result_path)
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")

        # print summary
        logger.info("\n===== BENCHMARK SUMMARY =====")
        for result in all_results:
            logger.info(f"{result.engine}:")
            logger.info(f"\tBypass rate: {result.bypass_rate * 100:.1f}%")
            logger.info(f"\tAverage memory: {result.average_memory_mb} MB")
            logger.info(f"\tAverage CPU: {result.average_cpu_percent:.1f}%")
            if result.error:
                logger.info(f"\tError: {result.error}")
    except Exception as e:
        logger.critical(f"Critical error in benchmark execution: {e}")
        raise
    finally:
        # clean up any remaining async tasks
        pending = [task for task in asyncio.all_tasks() if not task.done() and task != asyncio.current_task()]

        if pending:
            logger.info(f"Cancelling {len(pending)} pending tasks...")
            for task in pending:
                task.cancel()

            try:
                await asyncio.wait_for(asyncio.gather(*pending, return_exceptions=True), timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Some tasks did not complete within timeout")

        # force garbage collection
        gc.collect()


def main() -> None:
    try:
        asyncio.run(run_all_benchmarks())
    except KeyboardInterrupt:
        logger.info("Benchmark interrupted by user")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        raise


if __name__ == "__main__":
    main()
