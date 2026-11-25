import asyncio
import json
import os
import random
import secrets
import string
import time
from typing import Dict, Optional
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener, urlopen

import psutil
from patchright.async_api import async_playwright

from config.settings import settings
from engines.playwright_base import PlaywrightBase
from utils.js_script import load_js_script
from utils.process import find_new_child_processes
from utils.real_ip import get_real_ip


class KameleoEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "kameleo_chroma",
            base_url: str = "http://localhost:5050",
            headless: bool = False,
            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        """
        Initialize the KameleoEngine with the given parameters

        Every start creates a fresh profile from a Kameleo Windows/Chrome fingerprint, launches it in Kameleo's
        Chroma browser and deletes exactly that profile on stop. Requires Kameleo (desktop app or Docker image)
        running with its Local API.

        :param name: Name of the engine instance
        :param base_url: Kameleo Local API URL
        :param headless: Whether to run the browser in headless mode
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, "chromium", None, headless, proxy)
        self._base_url = base_url.rstrip("/")
        self._profile_id: Optional[str] = None

    @property
    def supported_proxy_protocols(self) -> list[str]:
        return ["http"]

    def _call(self, method: str, path: str, body: Optional[dict] = None) -> Optional[dict]:
        """Make a request to the Kameleo Local API"""

        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = Request(self._base_url + path, data=data, method=method, headers={"Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=120) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else None
        except HTTPError as e:
            raise RuntimeError(f"Kameleo API {method} {path} failed: {e.code} {e.read()[:300]!r}")

    def _proxy_location(self) -> dict:
        """
        Look up the proxy's exit IP, timezone and coordinates through the proxy itself

        Kameleo's own lookup for 'automatic' timezone/geolocation/WebRTC is refused by some proxy providers,
        so the same values are resolved here and set on the profile explicitly
        """

        proxy_url = (f"http://{self.proxy['username']}:{self.proxy['password']}@{self.proxy['host']}:{self.proxy['port']}"
                     if "username" in self.proxy else f"http://{self.proxy['host']}:{self.proxy['port']}")
        opener = build_opener(ProxyHandler({"http": proxy_url, "https": proxy_url}))
        with opener.open("http://ip-api.com/json/?fields=status,query,timezone,lat,lon", timeout=30) as resp:
            location = json.loads(resp.read())
        if location.get("status") != "success" or location.get("query") == get_real_ip():
            raise RuntimeError("Kameleo engine could not resolve the proxy's location")
        return location

    def _create_profile(self) -> str:
        """Create a fresh profile for this run and return its ID"""

        fingerprints = self._call("GET", "/fingerprints?deviceType=desktop&osFamily=windows&browserProduct=chrome")
        suffix = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        profile: dict = {
            "fingerprintId": random.choice(fingerprints)["id"],
            "name": f"benchmark-{self.name}-{suffix}",
            "tags": ["benchmark"],
        }
        if self.proxy:
            location = self._proxy_location()
            server = {"host": self.proxy["host"], "port": int(self.proxy["port"])}
            if "username" in self.proxy:
                server.update({"id": self.proxy["username"], "secret": self.proxy["password"]})
            profile.update({
                "proxy": {"value": "http", "extra": server},
                "timezone": {"value": "manual", "extra": location["timezone"]},
                "geolocation": {"value": "manual", "extra": {"latitude": location["lat"], "longitude": location["lon"]}},
                "webRtc": {"value": "manual", "extra": {"publicIp": location["query"], "privateIp": "192.168.1.23"}},
            })
        return self._call("POST", "/profiles/new", profile)["id"]

    def _delete_profile(self, profile_id: str) -> None:
        """Delete the profile created by this engine (only that ID)"""

        # retry: right after stop the profile may still be closing and the delete gets rejected
        for _ in range(5):
            try:
                self._call("DELETE", f"/profiles/{profile_id}")
                return
            except Exception:
                time.sleep(2)

    async def start(self) -> None:
        """Create a Kameleo profile, launch it, and connect via CDP"""

        self._start_time = asyncio.get_event_loop().time()

        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        self._profile_id = await asyncio.to_thread(self._create_profile)
        await asyncio.to_thread(
            self._call, "POST", f"/profiles/{self._profile_id}/start",
            {"arguments": ["--headless"] if self.headless else []}
        )

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.connect_over_cdp(
            f"ws://{urlparse(self._base_url).netloc}/playwright/{self._profile_id}"
        )
        self.context = self.browser.contexts[0]

        await self.context.add_init_script(await load_js_script('unlockShadowDom.js'))

        self.page = await self.context.new_page()
        self.page.set_default_timeout(settings.browser.action_timeout_s * 1000)
        self.page.set_default_navigation_timeout(settings.browser.page_load_timeout_s * 1000)

        process_children_after = parent_process.children(recursive=True)
        self.process_list = find_new_child_processes(process_children_before, process_children_after)

    async def stop(self) -> None:
        """Close page, disconnect browser, stop and delete the Kameleo profile"""

        try:
            if self.page:
                await self.page.close()
        except:
            pass
        self.page = None

        try:
            if self.browser:
                await self.browser.close()
        except:
            pass
        self.browser = None
        self.context = None

        try:
            if self.playwright:
                await self.playwright.stop()
        except:
            pass
        self.playwright = None

        if self._profile_id:
            try:
                await asyncio.to_thread(self._call, "POST", f"/profiles/{self._profile_id}/stop")
            except:
                pass
            await asyncio.to_thread(self._delete_profile, self._profile_id)
            self._profile_id = None

        self.process_list = None
