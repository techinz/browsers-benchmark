"""
TikTok Shop bypass test using kalodata persistent Chrome profile (has existing cookies).

Tests:
  1. patchright + kalodata profile → bypass rate / load time
  2. Rate limit probe: N requests in succession, measure drop rate

Usage:
    uv run python run_tiktok_with_profile.py
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

TIKTOK_SHOP_URL = "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja"
KALODATA_PROFILE = Path.home() / ".kalodata" / "profile-main"
STABILIZATION = 8  # seconds
RESULTS_DIR = Path("results/tiktok")

RATE_TEST_URLS = [
    "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja",
    "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja",
    "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja",
]


async def check_page_status(page) -> dict:
    """Return dict with bypass status and page details."""
    try:
        title = await page.title()
        captcha_count = await page.evaluate(
            "document.querySelectorAll('[class*=\"secsdk-captcha\"],.captcha_verify_container').length"
        )
        product_count = await page.evaluate(
            "document.querySelectorAll('.pdp-scroll-container,[data-testid=\"product-price\"],.price-area').length"
        )
        is_blocked = captcha_count > 0 or "Security Check" in title or "セキュリティ" in title
        return {
            "title": title,
            "captcha_count": captcha_count,
            "product_count": product_count,
            "bypass": not is_blocked and product_count > 0,
            "blocked": is_blocked,
        }
    except Exception as e:
        return {"error": str(e), "bypass": False, "blocked": True}


async def test_with_kalodata_profile():
    """Test using the existing kalodata profile which already has TikTok cookies."""
    from patchright.async_api import async_playwright

    print(f"\n=== kalodata プロファイルを使ったpatchrightテスト ===")
    print(f"profile: {KALODATA_PROFILE}")
    print(f"URL: {TIKTOK_SHOP_URL}\n")

    if not KALODATA_PROFILE.exists():
        print(f"❌ プロファイルが見つかりません: {KALODATA_PROFILE}")
        return None

    results = []

    async with async_playwright() as pw:
        ctx = await pw.chromium.launch_persistent_context(
            user_data_dir=str(KALODATA_PROFILE),
            channel="chrome",
            headless=False,
            no_viewport=True,
            locale="ja-JP",
            timezone_id="Asia/Tokyo",
            args=["--window-size=1280,900", "--window-position=-32000,-32000"],
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        for i, url in enumerate(RATE_TEST_URLS):
            t0 = time.time()
            await page.goto(url, wait_until="domcontentloaded", timeout=90_000)
            await page.wait_for_timeout(STABILIZATION * 1000)
            load_time = round(time.time() - t0, 2)

            status = await check_page_status(page)
            status["load_time"] = load_time
            status["attempt"] = i + 1
            results.append(status)

            mark = "✅ BYPASS" if status["bypass"] else ("⚠️ CAPTCHA" if status["blocked"] else "❓ UNKNOWN")
            print(f"  [{i+1}] {mark}  load={load_time}s  title={status.get('title','?')[:50]}")

            if status["blocked"]:
                print(f"       → captcha={status.get('captcha_count')} product={status.get('product_count')}")
                # Take screenshot for debugging
                screenshot_path = RESULTS_DIR / f"captcha_attempt_{i+1}.png"
                RESULTS_DIR.mkdir(parents=True, exist_ok=True)
                await page.screenshot(path=str(screenshot_path))
                print(f"       → screenshot: {screenshot_path}")

            await asyncio.sleep(3)  # between requests

        await ctx.close()

    return results


async def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    profile_results = await test_with_kalodata_profile()

    if profile_results:
        bypassed = sum(1 for r in profile_results if r.get("bypass"))
        print(f"\n=== 結果サマリー ===")
        print(f"kalodata profile: {bypassed}/{len(profile_results)} 成功")

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = RESULTS_DIR / f"tiktok_profile_{ts}.json"
        out.write_text(json.dumps(profile_results, ensure_ascii=False, indent=2))
        print(f"結果保存: {out}")


if __name__ == "__main__":
    asyncio.run(main())
