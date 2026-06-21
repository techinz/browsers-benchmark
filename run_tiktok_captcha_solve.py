"""
TikTok Shop E2E: patchright + CAPTCHA solver → product page access.

1. Navigate to shop.tiktok.com product page (always shows CAPTCHA on cold start)
2. Detect CAPTCHA → solve with OpenCV puzzle solver
3. Verify product page loaded
4. Measure: CAPTCHA solve time, total access time, bypass rate over N attempts

Usage:
    uv run python run_tiktok_captcha_solve.py
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "kalodata-scraper"))

TIKTOK_SHOP_URL = "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja"
N_ATTEMPTS = 3
RESULTS_DIR = Path("results/tiktok")


async def check_page_status(page) -> dict:
    try:
        title = await page.title()
        captcha_count = await page.evaluate(
            "document.querySelectorAll('[class*=\"secsdk-captcha\"],.captcha_verify_container').length"
        )
        is_captcha = captcha_count > 0 or "Security Check" in title or "Verify" == title.strip()
        # Real product title is always > 10 chars and contains product description
        is_product = not is_captcha and len(title) > 10 and title not in ("", "TikTok Shop")
        return {
            "title": title,
            "captcha_count": captcha_count,
            "bypass": is_product,
            "blocked": is_captcha,
        }
    except Exception as e:
        return {"error": str(e), "bypass": False, "blocked": True}


async def run_with_captcha_solver():
    from patchright.async_api import async_playwright

    # Import our CAPTCHA solver
    try:
        from kalodata.tiktok_captcha import solve_captcha_if_present
        print("✅ tiktok_captcha solver インポート成功")
    except ImportError as e:
        print(f"❌ CAPTCHA solver インポート失敗: {e}")
        print("   → ~/work/kalodata-scraper をPYTHONPATHに追加して再試行")
        return None

    print(f"\n=== patchright + CAPTCHA solver E2Eテスト ===")
    print(f"URL: {TIKTOK_SHOP_URL}")
    print(f"試行回数: {N_ATTEMPTS}\n")

    results = []

    async with async_playwright() as pw:
        # 一時的な新規プロファイル（クリーンな状態でCAPTCHAを確実に表示させる）
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            ctx = await pw.chromium.launch_persistent_context(
                user_data_dir=tmpdir,
                channel="chrome",
                headless=False,
                no_viewport=True,
                locale="ja-JP",
                timezone_id="Asia/Tokyo",
                args=["--window-size=1280,900"],
            )
            page = ctx.pages[0] if ctx.pages else await ctx.new_page()

            for attempt in range(N_ATTEMPTS):
                result = {"attempt": attempt + 1}
                t_start = time.time()

                print(f"--- 試行 {attempt + 1}/{N_ATTEMPTS} ---")

                # Navigate
                t_nav = time.time()
                await page.goto(TIKTOK_SHOP_URL, wait_until="domcontentloaded", timeout=90_000)
                await page.wait_for_timeout(3000)
                result["nav_time"] = round(time.time() - t_nav, 2)

                # Check initial state
                before = await check_page_status(page)
                result["initial_captcha"] = before["blocked"]
                print(f"  初期状態: {'⚠️ CAPTCHA' if before['blocked'] else '✅ クリア'} (nav={result['nav_time']}s)")

                # Solve CAPTCHA if present
                if before["blocked"]:
                    t_solve = time.time()
                    solved = await solve_captcha_if_present(page, max_attempts=4)
                    result["captcha_solve_time"] = round(time.time() - t_solve, 2)
                    result["captcha_solved"] = solved
                    print(f"  CAPTCHA解決: {'✅ 成功' if solved else '❌ 失敗'} ({result['captcha_solve_time']}s)")

                    await page.wait_for_timeout(3000)

                # Check after solve
                after = await check_page_status(page)
                result["final_bypass"] = after["bypass"]
                result["final_title"] = after.get("title", "")
                result["final_captcha_count"] = after.get("captcha_count", 0)
                result["final_product_count"] = after.get("product_count", 0)
                result["total_time"] = round(time.time() - t_start, 2)

                mark = "✅ BYPASS" if after["bypass"] else "❌ BLOCKED"
                print(f"  最終結果: {mark}  total={result['total_time']}s  title={after.get('title','?')[:50]}")

                # Screenshot
                RESULTS_DIR.mkdir(parents=True, exist_ok=True)
                shot = RESULTS_DIR / f"solve_attempt_{attempt+1}.png"
                await page.screenshot(path=str(shot))
                result["screenshot"] = str(shot)
                print(f"  スクリーンショット: {shot}")

                results.append(result)

                if attempt < N_ATTEMPTS - 1:
                    # Navigate back to force new CAPTCHA for next attempt
                    await page.goto("about:blank")
                    await asyncio.sleep(2)

            await ctx.close()

    return results


async def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    results = await run_with_captcha_solver()
    if not results:
        return

    bypassed = sum(1 for r in results if r.get("final_bypass"))
    solved = sum(1 for r in results if r.get("captcha_solved"))
    avg_solve = sum(r.get("captcha_solve_time", 0) for r in results) / len(results)
    avg_total = sum(r.get("total_time", 0) for r in results) / len(results)

    print(f"\n=== サマリー ===")
    print(f"CAPTCHA解決成功: {solved}/{len(results)}")
    print(f"バイパス成功:    {bypassed}/{len(results)}")
    print(f"平均CAPTCHA時間: {avg_solve:.1f}s")
    print(f"平均合計時間:    {avg_total:.1f}s")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RESULTS_DIR / f"tiktok_captcha_solve_{ts}.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n結果保存: {out}")


if __name__ == "__main__":
    asyncio.run(main())
