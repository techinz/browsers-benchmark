import asyncio
import json
import os
import time
from typing import Dict, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import psutil
from patchright.async_api import async_playwright

from config.settings import settings
from engines.playwright_base import PlaywrightBase
from utils.js_script import load_js_script
from utils.process import find_new_child_processes


class AdsPowerEngine(PlaywrightBase):
    def __init__(
            self,
            name: str = "adspower",
            api_key: str = "",
            base_url: str = "http://local.adspower.net:50325",
            group_id: str = "",
            headless: bool = False,
            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        super().__init__(name, "chromium", None, headless, proxy)
        self._api_key = api_key
        self._base_url = base_url.rstrip('/')
        self._group_id = group_id
        self._created_profile_id: Optional[str] = None

    @property
    def supported_proxy_protocols(self) -> list[str]:
        return ["http", "socks5"]

    def _api_call(self, method: str, endpoint: str, params: Optional[dict] = None, body: Optional[dict] = None) -> dict:
        """Make a GET or POST request to the AdsPower local API"""

        url = self._base_url + endpoint
        if params:
            url += '?' + urlencode(params)

        headers = {"Authorization": f"Bearer {self._api_key}"}
        if body is not None:
            data = json.dumps(body).encode('utf-8')
            headers["Content-Type"] = "application/json"
            req = Request(url, data=data, method=method, headers=headers)
        else:
            req = Request(url, method=method, headers=headers)

        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())

    def _create_profile(self) -> str:
        """Create a fresh AdsPower profile and return its ID"""

        profile_data: dict = {
            "name": f"benchmark-{self.name}",
            "group_id": self._group_id,
            "fingerprint_config": {
                "automatic_timezone": "1",
                "language_switch": "1",
                "webrtc": "proxy",
                "canvas": "1",
                "webgl_image": "1",
                "webgl": "3",
                "audio": "1",
                "screen_resolution": "random",
                "random_ua": {
                    "ua_system_version": ["Windows 10", "Windows 11"]
                },
            },
        }

        if self.proxy:
            proxy_config: dict = {
                "proxy_soft": "other",
                "proxy_type": self.proxy["protocol"],
                "proxy_host": self.proxy["host"],
                "proxy_port": str(self.proxy["port"]),
            }
            if "username" in self.proxy:
                proxy_config["proxy_user"] = self.proxy["username"]
            if "password" in self.proxy:
                proxy_config["proxy_password"] = self.proxy["password"]
            profile_data["user_proxy_config"] = proxy_config

        response = self._api_call("POST", "/api/v1/user/create", body=profile_data)
        if response.get("code") != 0:
            raise RuntimeError(f"AdsPower profile creation failed: {response.get('msg')}")
        return response["data"]["id"]

    def _delete_profile(self, profile_id: str) -> None:
        """Delete an AdsPower profile"""
        # retry: right after browser/stop a headed profile may still be closing and the delete gets rejected
        for _ in range(5):
            try:
                # the API expects a json body, query params are rejected with "user_ids is required"
                response = self._api_call("POST", "/api/v1/user/delete", body={"user_ids": [profile_id]})
                if response.get("code") == 0:
                    return
            except:
                pass
            time.sleep(2)

    async def start(self) -> None:
        """Create AdsPower profile, launch it, and connect via Playwright CDP"""

        self._start_time = asyncio.get_event_loop().time()

        parent_process = psutil.Process(os.getpid())
        process_children_before = parent_process.children(recursive=True)

        # create a fresh profile (with proxy if assigned by benchmark)
        self._created_profile_id = self._create_profile()

        # launch the profile via AdsPower local API
        launch_params: dict = {"user_id": self._created_profile_id}
        if self.headless:
            launch_params["headless"] = 1

        response = self._api_call("GET", "/api/v1/browser/start", params=launch_params)
        if response.get("code") != 0:
            self._delete_profile(self._created_profile_id)
            raise RuntimeError(f"AdsPower failed to launch profile: {response.get('msg')}")

        ws_endpoint = response["data"]["ws"]["puppeteer"]

        # connect to the running browser via CDP (patchright instead of playwright: it leaves fewer automation
        # traces, e.g. headless profiles connected with playwright get flagged for inconsistent timing resolution)
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.connect_over_cdp(ws_endpoint)
        self.context = self.browser.contexts[0]

        # inject shadow DOM unlock script for new pages
        await self.context.add_init_script(await load_js_script('unlockShadowDom.js'))

        self.page = await self.context.new_page()
        self.page.set_default_timeout(settings.browser.action_timeout_s * 1000)
        self.page.set_default_navigation_timeout(settings.browser.page_load_timeout_s * 1000)

        process_children_after = parent_process.children(recursive=True)
        self.process_list = find_new_child_processes(process_children_before, process_children_after)

    async def stop(self) -> None:
        """Close page, disconnect browser, stop and delete the AdsPower profile"""

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

        if self._created_profile_id:
            try:
                self._api_call("GET", "/api/v1/browser/stop", params={"user_id": self._created_profile_id})
            except:
                pass
            self._delete_profile(self._created_profile_id)
            self._created_profile_id = None

        self.process_list = None
