"""
TikTok Shop レート制限実測テスト。

CAPTCHAを1回解決してセッションを確立した後、
連続でN回アクセスしてレート制限のしきい値を調査。

Usage:
    uv run python run_tiktok_rate_test.py
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "kalodata-scraper"))

TIKTOK_SHOP_URL = "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja"
# テスト用に別の商品URLも用意（同じページのリロードだけだと非現実的なので）
ALT_URLS = [
    "https://shop.tiktok.com/view/product/1735770738026579444?region=JP&local=ja",
]
N_RAPID_REQUESTS = 20
DELAY_BETWEEN = 1.0  # 秒（最初は1秒間隔）
RESULTS_DIR = Path("results/tiktok")


async def check_blocked(page) -> bool:
    try:
        title = await page.title()
        captcha_n = await page.evaluate(
            "document.querySelectorAll('[class*=\"secsdk-captcha\"],.captcha_verify_container').length"
        )
        return captcha_n > 0 or "Security Check" in title or "Access Denied" in title or "403" in title
    except Exception:
        return True


async def main():
    from patchright.async_api import async_playwright
    from kalodata.tiktok_captcha import solve_captcha_if_present

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"TikTok Shop レート制限テスト — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"連続リクエスト数: {N_RAPID_REQUESTS}, 間隔: {DELAY_BETWEEN}s\n")

    results = []

    async with async_playwright() as pw:
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

            # Step 1: 初回アクセスでCAPTCHA解決
            print("=== Step 1: 初回CAPTCHA解決 ===")
            await page.goto(TIKTOK_SHOP_URL, wait_until="domcontentloaded", timeout=90_000)
            await page.wait_for_timeout(2000)

            if await check_blocked(page):
                print("CAPTCHAを解決中...")
                solved = await solve_captcha_if_present(page, max_attempts=5)
                if not solved:
                    print("❌ 初回CAPTCHA解決失敗。終了。")
                    await ctx.close()
                    return
                print("✅ CAPTCHA解決成功。セッション確立。\n")
            else:
                print("✅ CAPTCHAなし（既存セッション）\n")

            await page.wait_for_timeout(3000)

            # Step 2: 連続リクエストテスト
            print(f"=== Step 2: {N_RAPID_REQUESTS}回連続アクセス (間隔={DELAY_BETWEEN}s) ===")
            consecutive_blocked = 0

            for i in range(N_RAPID_REQUESTS):
                url = ALT_URLS[i % len(ALT_URLS)]
                t0 = time.time()

                await page.goto(url, wait_until="domcontentloaded", timeout=90_000)
                await page.wait_for_timeout(1500)

                load_time = round(time.time() - t0, 2)
                blocked = await check_blocked(page)
                title = await page.title()

                r = {
                    "req": i + 1,
                    "blocked": blocked,
                    "load_time": load_time,
                    "title": title[:50],
                }
                results.append(r)

                mark = "❌ BLOCKED" if blocked else "✅ OK"
                print(f"  [{i+1:02d}] {mark}  {load_time}s  {title[:40]}")

                if blocked:
                    consecutive_blocked += 1
                    if consecutive_blocked >= 3:
                        print(f"\n⛔ {consecutive_blocked}回連続ブロック — レート制限に達した可能性。終了。")
                        break
                else:
                    consecutive_blocked = 0

                if i < N_RAPID_REQUESTS - 1:
                    await asyncio.sleep(DELAY_BETWEEN)

            await ctx.close()

    # サマリー
    total = len(results)
    ok_count = sum(1 for r in results if not r["blocked"])
    blocked_count = total - ok_count
    avg_load = sum(r["load_time"] for r in results) / total if total else 0

    print(f"\n=== レート制限テスト結果 ===")
    print(f"成功: {ok_count}/{total}")
    print(f"ブロック: {blocked_count}/{total}")
    print(f"平均ロード時間: {avg_load:.2f}s")
    print(f"リクエスト間隔: {DELAY_BETWEEN}s")

    first_block = next((r["req"] for r in results if r["blocked"]), None)
    if first_block:
        print(f"初回ブロック: {first_block}回目")
    else:
        print(f"ブロックなし（{N_RAPID_REQUESTS}回完走）")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RESULTS_DIR / f"tiktok_rate_{ts}.json"
    out.write_text(json.dumps({
        "config": {"n_requests": N_RAPID_REQUESTS, "delay_s": DELAY_BETWEEN},
        "summary": {"ok": ok_count, "blocked": blocked_count, "avg_load": avg_load, "first_block": first_block},
        "requests": results,
    }, ensure_ascii=False, indent=2))
    print(f"\n結果保存: {out}")


if __name__ == "__main__":
    asyncio.run(main())
