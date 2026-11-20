import asyncio
import gc
import logging
import os
import shutil
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
from utils.proxy.proxy_manager import proxy_manager, is_proxy_related_error, handle_proxy_fallback
from utils.report import generate_report
from utils.real_ip import detect_real_ip
from utils.screenshot import take_screenshot

setup_logging()

logger = logging.getLogger(__name__)

# hard limit for a single target (navigation + checks + proxy fallbacks + screenshot), so a dead proxy can't hang the run
TARGET_TIMEOUT_S = 600


async def navigate_with_retry(engine: BrowserEngine, url: str, retries: int = 2) -> Dict[str, Any]:
    """
    Navigate to url, retrying when the navigation was aborted by a late redirect of the previous page
    (e.g. a Cloudflare challenge that finishes after we already moved on)

    :param engine: The browser engine to use
    :param url: URL to navigate to
    :param retries: How many times to retry an aborted navigation
    """

    aborted_markers = ("ns_binding_aborted", "err_aborted", "interrupted by another navigation")
    for attempt in range(retries + 1):
        try:
            return await engine.navigate(url)
        except Exception as e:
            if attempt == retries or not any(m in str(e).lower() for m in aborted_markers):
                raise
            logger.info(f"{engine.name}: navigation to {url} was aborted ({e}), retrying...")
            await asyncio.sleep(3)


async def test_bypass_target(
        engine: BrowserEngine,
        target: Dict[str, Any],
        screenshots_path: str
) -> BypassTestResult:
    """
    Test a single bypass target

    :param engine: The browser engine to use
    :param target: The target configuration to test
    :param screenshots_path: Path to save screenshots
    """

    logger.info(f"Testing {engine.name} against {target['name']}...")

    result = BypassTestResult(target=target["name"], url=target["url"])

    async def attempt_bypass_test():
        navigation_result = await navigate_with_retry(engine, target["url"])
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
        result = await attempt_bypass_test()
    except Exception as e:
        # check if this is a proxy-related error that warrants fallback
        if is_proxy_related_error(e) and settings.proxy.enabled:
            fallback_result, error_msg = await handle_proxy_fallback(
                engine, target['name'], e, attempt_bypass_test
            )
            if fallback_result:
                result = fallback_result
            else:
                result.error = error_msg
        else:
            # non-proxy error - just record it
            result.error = str(e)
            logger.warning(f'{engine.name} failed bypass test for {target["name"]}: {e}')

    await take_screenshot(engine, screenshots_path, target["name"])

    return result


async def extract_browser_data(
        engine: BrowserEngine,
        target: Dict[str, Any],
        screenshots_path: str
) -> BrowserDataResult:
    """
    Extract browser data from a target

    :param engine: The browser engine to use
    :param target: The target configuration to extract data from
    :param screenshots_path: Path to save screenshots
    """

    logger.info(f"Extracting browser data from {target['name']} using {engine.name}...")

    result = BrowserDataResult(target=target["name"], url=target["url"])

    async def attempt_data_extraction():
        await navigate_with_retry(engine, target["url"])
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
        result = await attempt_data_extraction()
    except Exception as e:
        # check if this is a proxy-related error that warrants fallback
        if is_proxy_related_error(e) and settings.proxy.enabled:
            fallback_result, error_msg = await handle_proxy_fallback(
                engine, target['name'], e, attempt_data_extraction
            )
            if fallback_result:
                result = fallback_result
            else:
                result.error = error_msg
        else:
            # non-proxy error, just record it
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
    """
    Run benchmark for a browser engine

    :param engine_cls: The browser engine class to instantiate
    :param engine_params: Parameters for the engine
    :param bypass_targets: List of bypass targets to test
    :param browser_data_targets: List of browser data targets to test
    :param screenshots_path: Path for saving screenshots
    :param proxy: Optional proxy configuration to use for the engine
    """

    if proxy:
        engine_params = {**engine_params, "proxy": proxy}

    engine = engine_cls(**engine_params)
    engine_screenshots_path = os.path.join(screenshots_path, engine.name)

    if os.path.exists(engine_screenshots_path):
        shutil.rmtree(engine_screenshots_path, ignore_errors=True)  # clear previous data if exists

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
            try:
                bypass_result = await asyncio.wait_for(
                    test_bypass_target(engine, target, engine_screenshots_path), TARGET_TIMEOUT_S)
            except asyncio.TimeoutError:
                logger.warning(f"{engine.name} timed out on {target['name']} after {TARGET_TIMEOUT_S}s")
                bypass_result = BypassTestResult(target=target["name"], url=target["url"],
                                                 error=f"Target timed out after {TARGET_TIMEOUT_S}s")
            results.bypass_targets_results.append(bypass_result)

            if not bypass_result.error:
                memory_readings.append(bypass_result.performance.memory_mb)
                cpu_readings.append(bypass_result.performance.cpu_percent)

            await asyncio.sleep(1)

        # extract browser data
        for target in browser_data_targets:
            try:
                data_result = await asyncio.wait_for(
                    extract_browser_data(engine, target, engine_screenshots_path), TARGET_TIMEOUT_S)
            except asyncio.TimeoutError:
                logger.warning(f"{engine.name} timed out on {target['name']} after {TARGET_TIMEOUT_S}s")
                data_result = BrowserDataResult(target=target["name"], url=target["url"],
                                                error=f"Target timed out after {TARGET_TIMEOUT_S}s")
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

    # the machine's real IP is replaced with a placeholder in results and screenshots
    detect_real_ip()

    # validate proxy setup before starting
    if not settings.proxy.enabled:
        logger.warning("PROXIES ARE DISABLED! Results may be inaccurate due to IP reputation.")
        logger.warning("\tEnable proxies in .env for reliable benchmark results.")
    else:
        # check if we have enough compatible proxies for all engines
        engines_with_protocols = []
        for engine_config in engines_config.engines:
            engine_cls = engine_config["class"]
            # create temporary instance to get supported protocols
            temp_engine = engine_cls(**engine_config["params"])
            engines_with_protocols.append((
                engine_config['params']['name'],
                temp_engine.supported_proxy_protocols
            ))

        if not proxy_manager.validate_proxy_count_by_protocol(engines_with_protocols):
            logger.error("PROXY VALIDATION FAILED!\n"
                         "Some engines don't have compatible proxies available.\n"
                         "Please:\n"
                         "\tAdd more proxies with the required protocols to documents/proxies.txt\n"
                         "\tOr disable those engines in config/engines.py\n"
                         "\tOr disable proxy usage by setting PROXY_ENABLED=false in .env")
            raise Exception("Not enough compatible proxies for the configured engines!")

        logger.info("Proxy protocol validation passed for all engines")

    timestamp = datetime.now().strftime("%Y.%m.%d")
    result_path, media_path, screenshots_path = create_directory_structure(timestamp)

    try:
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
                # create temporary instance to get supported protocols
                temp_engine = engine_config["class"](**engine_config["params"])
                supported_protocols = temp_engine.supported_proxy_protocols

                if supported_protocols:
                    proxy = proxy_manager.get_proxy_by_protocol(supported_protocols)
                    if not proxy:
                        logger.error(f"No compatible proxy available for {engine_name}")
                        logger.error(f"\tEngine supports: {', '.join(supported_protocols)}")

                        # show what proxies are available
                        stats = proxy_manager.get_stats()
                        if stats['available'] > 0:
                            logger.error(f"\t{stats['available']} proxies remain, but none with compatible protocols")
                        else:
                            logger.error(f"\tNo proxies remaining (used: {stats['used']}, failed: {stats['failed']})")

                        logger.error(f"\tSkipping {engine_name}...")
                        continue
                    else:
                        logger.info(f"Assigned {proxy['protocol']} proxy to {engine_name}")

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
            except Exception as e:
                logger.error(f"Failed to run benchmark for {engine_name}: {e}")

                results = BenchmarkResults(
                    engine=engine_name,
                    timestamp=datetime.now().isoformat(),
                    error=str(e)
                )

            if results:
                # save and report results
                results_path = save_results(results, result_path)
                logger.info(f"\nResults for {engine_name} saved to {results_path}")

                # generate report
                try:
                    generate_report(results_path, result_path)
                except Exception as e:
                    logger.error(f"Failed to generate report: {e}")

            # print summary
            logger.info(f"\n===== BENCHMARK FOR {engine_name} SUMMARY =====")
            logger.info(f"{results.engine}:")
            logger.info(f"\tBypass rate: {results.bypass_rate * 100:.1f}%")
            logger.info(f"\tAverage memory: {results.average_memory_mb} MB")
            logger.info(f"\tAverage CPU: {results.average_cpu_percent:.1f}%")
            if results.error:
                logger.info(f"\tError: {results.error}")

            # print proxy statistics if enabled
            if settings.proxy.enabled:
                proxy_stats = proxy_manager.get_stats()
                logger.info("\n===== PROXY STATISTICS =====")
                logger.info(f"Total proxies loaded: {proxy_stats['total_loaded']}")
                logger.info(f"Proxies used: {proxy_stats['used']}")
                logger.info(f"Proxies failed: {proxy_stats['failed']}")
                logger.info(f"Proxies remaining: {proxy_stats['available']}")

                if proxy_stats['failed'] > 0:
                    logger.warning(f"{proxy_stats['failed']} proxies failed during benchmarking")
                if proxy_stats['available'] == 0 and proxy_stats['failed'] > 0:
                    logger.warning("All proxies have been exhausted or failed")
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

        # force garbage collection (from some not properly closed browser instances)
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
