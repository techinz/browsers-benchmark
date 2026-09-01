"""
TikTok Shop bypass benchmark — patchright / camoufox / playwright (headless+headed).

Usage:
    uv run python run_tiktok_benchmark.py
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

TIKTOK_SHOP_URL = "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja"
STABILIZATION_DELAY = 8  # seconds — TikTok JS is heavy
RESULTS_DIR = Path("results/tiktok")


async def test_engine(engine, url: str, stabilization_delay: int) -> dict:
    result = {
        "engine": engine.name,
        "url": url,
        "bypass": False,
        "load_time": None,
        "error": None,
        "timestamp": datetime.now().isoformat(),
    }
    try:
        await engine.start()
        nav = await engine.navigate(url)
        result["load_time"] = round(nav["load_time"], 2)
        await asyncio.sleep(stabilization_delay)

        # check bypass
        from utils.targets.check_bypass.tiktok_shop import check_tiktok_shop_bypass
        result["bypass"] = await check_tiktok_shop_bypass(engine)

        # page details for debugging
        try:
            result["page_title"] = await engine.execute_js("return document.title")
            result["captcha_count"] = await engine.execute_js(
                "return document.querySelectorAll('[class*=\"secsdk-captcha\"]').length"
            )
            result["product_count"] = await engine.execute_js(
                "return document.querySelectorAll('.pdp-scroll-container,[data-testid=\"product-price\"]').length"
            )
        except Exception:
            pass

    except Exception as e:
        result["error"] = str(e)[:200]
    finally:
        try:
            await engine.stop()
        except Exception:
            pass

    status = "✅ BYPASS" if result["bypass"] else "❌ BLOCKED"
    print(f"  {status}  {engine.name:45s}  load={result.get('load_time','?')}s  err={result['error'] or '-'}")
    return result


async def main():
    from engines.playwright.patchright_engine import PatchrightEngine
    from engines.playwright.playwright_engine import PlaywrightEngine
    from engines.playwright.camoufox_engine import CamoufoxEngine

    engines = [
        PatchrightEngine(name="patchright_headless", headless=True),
        PatchrightEngine(name="patchright_headed", headless=False),
        CamoufoxEngine(name="camoufox_headless", headless=True),
        CamoufoxEngine(name="camoufox_headed", headless=False),
        PlaywrightEngine(name="playwright_headless", headless=True, browser_type="chromium"),
        PlaywrightEngine(name="playwright_headed", headless=False, browser_type="chromium"),
    ]

    print(f"\nTikTok Shop Bypass Benchmark — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {TIKTOK_SHOP_URL}")
    print("-" * 80)

    results = []
    for engine in engines:
        r = await test_engine(engine, TIKTOK_SHOP_URL, STABILIZATION_DELAY)
        results.append(r)
        await asyncio.sleep(3)  # cooldown between engines

    print("-" * 80)
    bypassed = [r for r in results if r["bypass"]]
    print(f"\n結果: {len(bypassed)}/{len(results)} エンジンがバイパス成功\n")
    for r in results:
        mark = "✅" if r["bypass"] else "❌"
        print(f"  {mark} {r['engine']}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RESULTS_DIR / f"tiktok_shop_{ts}.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n結果保存: {out}")


if __name__ == "__main__":
    asyncio.run(main())
