"""CloakBrowser BAN 対策 PoC ランナー(非破壊・スコープ限定)。

marketing-scraper / kalodata の BAN 対策候補として CloakBrowser を評価する。
共有 config を変更せず、対象エンジン(cloak/patchright × headless/headed)を
CF/DataDome 保護サイトへ当て、bypass 成否・automation fingerprint マーカー・
使用IP を計測する。第三者検出テストサイトのみ。自社アカウント・kalodata本番経路は触れない。
"""
import asyncio
import json
import os
import sys
from datetime import datetime

# home IP baseline: proxy 検証を確実に無効化(専用ランナーは proxy_manager を通さないが念のため)
os.environ["PROXY_ENABLED"] = "false"

from engines.playwright.cloakbrowser_engine import CloakBrowserEngine
from engines.playwright.patchright_engine import PatchrightEngine
from utils.targets.check_bypass.cloudflare_protected import check_cloudflare_bypass
from utils.targets.check_bypass.datadome_protected import check_datadome_bypass
from utils.targets.check_bypass.datadome_protected_2 import check_datadome2_bypass

ENGINES = [
    ("cloakbrowser_headless", CloakBrowserEngine, {"headless": True,  "name": "cloakbrowser_headless"}),
    ("cloakbrowser_headed",   CloakBrowserEngine, {"headless": False, "name": "cloakbrowser"}),
    ("patchright_headless",   PatchrightEngine,   {"headless": True,  "name": "patchright_headless"}),
    ("patchright_headed",     PatchrightEngine,   {"headless": False, "name": "patchright"}),
]

BYPASS_TARGETS = [
    ("cloudflare",        "https://community.cloudflare.com",       check_cloudflare_bypass),
    ("datadome",          "https://datadome.co/customers-stories/", check_datadome_bypass),
    ("datadome2_hermes",  "https://www.hermes.com/",                check_datadome2_bypass),
]

# automation マーカー直読み — CloakBrowser の source-level fingerprint パッチの効きを可視化
FP_JS = """
return {
  webdriver: navigator.webdriver,
  ua: navigator.userAgent,
  languages: navigator.languages,
  plugins: navigator.plugins.length,
  hasChrome: !!window.chrome,
  hardwareConcurrency: navigator.hardwareConcurrency,
  platform: navigator.platform,
  vendor: navigator.vendor
};
"""

PER_TARGET_TIMEOUT = 90  # 秒: 1ターゲットのハングで全体を止めない


async def probe_engine(label, cls, params):
    rec = {"engine": label, "params": {k: v for k, v in params.items() if k != "name"},
           "started_at": datetime.now().isoformat(), "targets": {}, "fingerprint": None,
           "ip": None, "fatal_error": None}
    engine = cls(**params)
    try:
        await asyncio.wait_for(engine.start(), timeout=120)
    except Exception as e:
        rec["fatal_error"] = f"start failed: {e!r}"
        return rec

    try:
        # 1) fingerprint probe(中立ページ)
        try:
            await asyncio.wait_for(engine.navigate("https://example.com"), timeout=PER_TARGET_TIMEOUT)
            rec["fingerprint"] = await engine.execute_js(FP_JS)
        except Exception as e:
            rec["fingerprint"] = {"error": repr(e)}

        # 2) bypass ターゲット
        for name, url, check in BYPASS_TARGETS:
            entry = {"url": url}
            try:
                nav = await asyncio.wait_for(engine.navigate(url), timeout=PER_TARGET_TIMEOUT)
                entry["load_time_ms"] = int(nav.get("load_time", 0) * 1000)
                entry["http_ok"] = nav.get("success")
                await asyncio.sleep(2)
                entry["bypass"] = await asyncio.wait_for(check(engine), timeout=PER_TARGET_TIMEOUT)
                entry["memory_mb"] = int(engine.get_memory_usage())
            except Exception as e:
                entry["error"] = repr(e)
                entry["bypass"] = None
            rec["targets"][name] = entry
            await asyncio.sleep(1)

        # 3) 使用IP透明化
        try:
            await asyncio.wait_for(engine.navigate("https://api.ipify.org?format=json"), timeout=PER_TARGET_TIMEOUT)
            await asyncio.sleep(2)
            found, html = await engine.locator("pre")
            rec["ip"] = json.loads(html).get("ip") if found else None
        except Exception as e:
            rec["ip"] = {"error": repr(e)}
    finally:
        try:
            await engine.stop()
        except Exception:
            pass
    return rec


async def main():
    results = {"run_at": datetime.now().isoformat(), "mode": "home-IP baseline (no proxy)",
               "note": "third-party bot-detection test sites only; no kalodata/production accounts touched",
               "engines": []}
    for label, cls, params in ENGINES:
        print(f"\n===== {label} =====", flush=True)
        rec = await probe_engine(label, cls, params)
        results["engines"].append(rec)
        # 逐次サマリ
        fp = rec.get("fingerprint") or {}
        print(f"  fatal={rec['fatal_error']}  ip={rec.get('ip')}", flush=True)
        print(f"  fp: webdriver={fp.get('webdriver')} plugins={fp.get('plugins')} "
              f"hasChrome={fp.get('hasChrome')} ua={str(fp.get('ua'))[:70]}", flush=True)
        for n, e in rec["targets"].items():
            print(f"  {n:18} bypass={e.get('bypass')} load={e.get('load_time_ms')}ms err={e.get('error')}", flush=True)

    out_dir = os.path.join(os.path.dirname(__file__), "results", "cloak-poc")
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(out_dir, f"cloak-poc-{stamp}.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved: {out_path}", flush=True)
    return out_path


if __name__ == "__main__":
    asyncio.run(main())
