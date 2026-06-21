"""
全プラットフォーム アクセス・ボット検出 サーベイ。

対象: Fastmoss, Astream, TikTok(本家), Instagram
patchright headed + headless の両方でテスト。
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

PLATFORMS = [
    {
        "name": "fastmoss",
        "url": "https://fastmoss.com/",
        "selectors": {
            "blocked": ["[id*='challenge']", ".cf-browser-verification", "[class*='captcha']"],
            "success": [".home", "nav", "header", ".logo"],
        },
    },
    {
        "name": "astream",
        "url": "https://astream.io/",
        "selectors": {
            "blocked": ["[id*='challenge']", ".cf-browser-verification"],
            "success": ["nav", "header", ".hero", "main"],
        },
    },
    {
        "name": "tiktok_main",
        "url": "https://www.tiktok.com/",
        "selectors": {
            "blocked": ["[class*='secsdk-captcha']", "[id*='challenge']", ".captcha_verify_container"],
            "success": ["[data-e2e='nav-logo']", ".tiktok-logo", "[class*='NavBar']"],
        },
    },
    {
        "name": "tiktok_creator",
        "url": "https://www.tiktok.com/@nintendo",
        "selectors": {
            "blocked": ["[class*='secsdk-captcha']", "[id*='challenge']"],
            "success": ["[data-e2e='user-post-item']", "[data-e2e='user-avatar']", "[class*='UserPage']"],
        },
    },
    {
        "name": "instagram_main",
        "url": "https://www.instagram.com/",
        "selectors": {
            "blocked": ["[class*='captcha']", "[id*='challenge']", "checkpoint"],
            "success": ["[aria-label='Instagram']", "nav", "[role='navigation']", "._9eogI"],
        },
    },
    {
        "name": "instagram_creator",
        "url": "https://www.instagram.com/nintendo/",
        "selectors": {
            "blocked": ["[class*='captcha']", "[id*='challenge']"],
            "success": ["[class*='ProfilePage']", "header section", "._aacl"],
        },
    },
]

RESULTS_DIR = Path("results/platforms")


async def count_el(page, selector: str) -> int:
    try:
        return await page.evaluate(
            f"document.querySelectorAll({repr(selector)}).length"
        )
    except Exception:
        return 0


async def detect_antibot(page) -> str:
    """アンチボットシステムを推定"""
    try:
        title = await page.title()
        url = page.url
        # page source snippet
        src = await page.evaluate("document.documentElement.innerHTML.slice(0, 3000)")
    except Exception:
        return "unknown"

    src_lower = src.lower()
    if "just a moment" in title.lower() or "__cf_chl" in url or "cf-browser-verification" in src_lower:
        return "cloudflare"
    if "datadome" in src_lower:
        return "datadome"
    if "akamai" in src_lower or "bm-verify" in src_lower:
        return "akamai"
    if "imperva" in src_lower or "incapsula" in src_lower:
        return "imperva"
    if "secsdk" in src_lower or "captcha_verify" in src_lower:
        return "tiktok_secsdk"
    if "security check" in title.lower():
        return "tiktok_secsdk"
    if "recaptcha" in src_lower:
        return "recaptcha"
    if "hcaptcha" in src_lower:
        return "hcaptcha"
    return "none_detected"


async def test_platform(page, platform: dict, headless: bool) -> dict:
    result = {
        "name": platform["name"],
        "url": platform["url"],
        "headless": headless,
        "blocked": False,
        "success": False,
        "antibot": "unknown",
        "load_time": None,
        "title": None,
        "error": None,
    }
    try:
        t0 = time.time()
        await page.goto(platform["url"], wait_until="domcontentloaded", timeout=60_000)
        await page.wait_for_timeout(4000)
        result["load_time"] = round(time.time() - t0, 2)
        result["title"] = (await page.title())[:60]
        result["antibot"] = await detect_antibot(page)

        # blocked?
        for sel in platform["selectors"]["blocked"]:
            if await count_el(page, sel):
                result["blocked"] = True
                break

        # success?
        for sel in platform["selectors"]["success"]:
            if await count_el(page, sel):
                result["success"] = True
                break

        # screenshot
        shot = RESULTS_DIR / f"{platform['name']}_{'hl' if headless else 'hd'}.png"
        await page.screenshot(path=str(shot), full_page=False)
        result["screenshot"] = str(shot)

    except Exception as e:
        result["error"] = str(e)[:200]

    mode = "headless" if headless else "headed"
    status = "✅" if result["success"] and not result["blocked"] else ("⚠️ " if result["blocked"] else "❓")
    print(f"  {status} [{mode:8s}] {platform['name']:22s}  antibot={result['antibot']:16s}  load={result.get('load_time','?')}s  title={result.get('title','?')[:35]}")
    return result


async def run_for_headless(headless: bool) -> list:
    from patchright.async_api import async_playwright
    import tempfile

    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        async with async_playwright() as pw:
            ctx = await pw.chromium.launch_persistent_context(
                user_data_dir=tmpdir,
                channel="chrome",
                headless=headless,
                no_viewport=True,
                locale="ja-JP",
                timezone_id="Asia/Tokyo",
                args=["--window-size=1280,900"],
            )
            page = ctx.pages[0] if ctx.pages else await ctx.new_page()

            for platform in PLATFORMS:
                r = await test_platform(page, platform, headless)
                results.append(r)
                await asyncio.sleep(2)

            await ctx.close()
    return results


async def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n===  プラットフォーム アクセス サーベイ  ===")
    print(f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"エンジン: patchright (headless + headed)\n")

    print("--- headed ---")
    headed_results = await run_for_headless(False)

    print("\n--- headless ---")
    headless_results = await run_for_headless(True)

    all_results = headed_results + headless_results

    print(f"\n{'='*70}")
    print(f"{'Platform':<22} {'headed':^10} {'headless':^10} {'AntiBot':<16}")
    print(f"{'-'*70}")
    for p in PLATFORMS:
        h = next((r for r in headed_results if r["name"] == p["name"]), {})
        hl = next((r for r in headless_results if r["name"] == p["name"]), {})
        h_ok = "✅" if h.get("success") and not h.get("blocked") else ("❌" if h.get("blocked") else "❓")
        hl_ok = "✅" if hl.get("success") and not hl.get("blocked") else ("❌" if hl.get("blocked") else "❓")
        print(f"  {p['name']:<20} {h_ok:^10} {hl_ok:^10} {h.get('antibot','?'):<16}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RESULTS_DIR / f"platform_survey_{ts}.json"
    out.write_text(json.dumps(all_results, ensure_ascii=False, indent=2))
    print(f"\n結果保存: {out}")


if __name__ == "__main__":
    asyncio.run(main())
