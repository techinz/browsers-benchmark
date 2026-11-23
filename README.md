# Browser Engine Benchmark

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A toolkit for testing browser automation engines against modern web protection systems. It checks how well each engine can bypass bot detection and measures their speed, resource usage, and resistance to fingerprinting.

<i>(Need some help with <b>Automation</b>? You can  <a href="https://automation.techinz.dev">hire me</a> for custom development or consulting!)</i>

## 🎯 Overview
Modern web applications use advanced bot detection like Cloudflare, DataDome, and Imperva to block automated access. This benchmark suite shows how different browser automation engines handle these defenses:
- **Bypass Success Rate**: Effectiveness against major protection systems
- **Performance Metrics**: Memory usage, CPU consumption, and page load times
- **Bot Detection Tests**: How 9 public bot/fingerprint test sites classify each engine (human, suspicious or bot)
- **Fingerprinting Resistance**: reCAPTCHA v3 scores
- **Network Analysis**: IP detection (proxy validation) and WebRTC leak testing

## 🚀 Key Features
### Protection System Testing
- **Cloudflare** 
- **DataDome**   
- **Amazon** 
- **Google Search** 
- **Ticketmaster (Imperva)**
- **Akamai**
- **PerimeterX / HUMAN Security**
- **Kasada**
- **Reddit**
- <i>More systems coming soon</i>

### Bot Detection Tests
Each site's own verdict is used, mapped to ✅ looks human, ⚠️ suspicious or ❌ detected as bot:
- **CleanTalk** - Human Score (80+ human, 50-79 needs review, below 50 bot)
- **Scrapfly** - automation signals (any DETECTED - bot, any SUSPICIOUS - suspicious)
- **BrowserScan** - bot detection checks (any Abnormal - bot)
- **APIVoid** - risk score and level (also weighs the IP reputation)
- **Pixelscan** - "You're Definitely a Human" or "Bot Behavior Detected"
- **Sannysoft** - passed/warn/failed checks
- **CreepJS** - headless and stealth detection (any non-zero percentage - bot)
- **DeviceAndBrowserInfo** - isBot and the individual detection signals
- **Fingerprint-Scan** - bot score categories (any HIGH - bot, any MEDIUM - suspicious)

Pages are only read (and buttons clicked) through JavaScript, the same way for every engine, so there is no real mouse movement - sites that score interaction see none.

Each engine also gets a **detection risk** (0 - human, 100 - bot): the average over the tests of the site's own score where it has one (CleanTalk, APIVoid, CreepJS, Fingerprint-Scan), otherwise its verdict (✅ 0, ⚠️ 50, ❌ 100). It ranks the engines, so a suspicious result counts too, not only an outright detection.

### Browser Engine Support
- <a href="https://www.adspower.com">**AdsPower**</a> - <b>(Proprietary)</b> Anti-detect browser with per-profile fingerprinting. Requires AdsPower desktop app running locally and an API key.
- <a href="https://playwright.dev">**Playwright**</a> - <b>(Open-Source)</b> Microsoft's automation framework (Chrome, Firefox, Safari)
- <a href="https://camoufox.com">**Camoufox**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python">**Patchright**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/tinyfish-io/tf-playwright-stealth">**Playwright Stealth**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/CloakHQ/cloakbrowser">**CloakBrowser**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/feder-cr/invisible_playwright">**invisible_playwright**</a> - <b>(Open-Source)</b> Playwright-based, patched Firefox with source-level fingerprint
- <a href="https://github.com/clearcotelabs/clearcote-browser">**Clearcote**</a> - <b>(Open-Source)</b> Playwright-based. Runs the open build without a key; `CLEARCOTE_LICENSE_KEY` switches to the licensed build
- <a href="https://github.com/ProxyShard/ShardBrowser">**ShardBrowser**</a> - <b>(Open-Source launcher)</b> Patched Chromium driven over CDP with Patchright, fingerprint profiles from its bundled library
- <a href="https://www.selenium.dev">**Selenium**</a> - <b>(Open-Source)</b> Browser automation framework (apparently deprecated, so it is tested without proxies)
- <a href="https://seleniumbase.io/">**Seleniumbase**</a> - <b>(Open-Source)</b> Professional toolkit for web automation activities
- <a href="https://github.com/ultrafunkamsterdam/nodriver">**NoDriver**</a> - <b>(Open-Source)</b> Browser automation framework (supports only SOCKS5 proxies)
- <a href="https://github.com/cdpdriver/zendriver">**ZenDriver**</a> - <b>(Open-Source)</b> NoDriver-based
- <a href="https://github.com/autoscrape-labs/pydoll">**PyDoll**</a> - <b>(Open-Source)</b> Asynchronous browser automation framework using Chrome DevTools Protocol (CDP) directly
- <i>More engines coming soon. What engine should I add next?</i>

### Analytics
- Automated report generation with visualizations
- Performance profiling and resource usage tracking
- Exportable results in JSON and Markdown formats

## 🔒 **Important: Proxy Requirements**
**Using a clean proxy is essential for accurate benchmark results.**
<details>
<summary>Why Proxies Are Required</summary>

- **IP Reputation**: Your home/datacenter IP may already be flagged by protection systems from previous automation attempts, browser extensions, or security software
- **Clean Testing Environment**: A fresh proxy IP ensures you're testing the browser engine's capabilities, not your IP's reputation
- **Rate Limiting**: Repeated tests from the same IP can trigger rate limiting, affecting bypass success rates
</details>

---

<div align="center">

<a href="https://www.rapidproxy.io/?ref=benchmark">
  <img width="600" height="314" alt="RapidProxy" src="https://github.com/user-attachments/assets/a9b19942-e868-4758-92b0-b7dc7cf0e97b" />
</a>

**RapidProxy — a high-performance proxy provider built for developers working on web scraping, browser automation, multi-account management, and large-scale data collection. 90M+ global residential IPs, native static ISP proxies, smart rotation, stable sessions, high concurrency, and non-expiring residential proxy traffic. Residential proxies start from $0.55/GB — use code `RAPID10` for 10% off.**

🔗 [https://www.rapidproxy.io](https://www.rapidproxy.io/?ref=benchmark)

</div>

---

## 📊 Sample Results
This benchmark provides detailed comparative analysis. Here's an excerpt from a recent test run (more in <a href="results/example">results/example</a>):  
<i>Real IP in this example is hidden and shown as REAL_IP (AdsPower engines were run on a separate machine)</i>  
<i>Proxy IP in this example is different for each engine</i>

## Overall Ranking
Overall score is the average of the bypass rate and 100 minus the detection risk (see Bot Detection Tests), both weighted equally.

| Engine | Overall score | Bypass Rate (%) | Detected by | Detection risk |
|-----------------|--------------:|----------------:|------------:|---------------:|
| invisible-playwright_headless | 89.2 | 80.0 | 0/9 | 2 |
| invisible-playwright | 88.1 | 80.0 | 0/9 | 4 |
| camoufox | 84.9 | 90.0 | 1/9 | 20 |
| camoufox_headless | 81.3 | 80.0 | 0/9 | 17 |
| clearcote_headless | 77.8 | 70.0 | 0/9 | 14 |
| patchright | 74.7 | 80.0 | 1/9 | 31 |
| pydoll-chrome | 73.9 | 80.0 | 1/9 | 32 |
| zendriver-chrome | 70.8 | 70.0 | 1/9 | 28 |
| clearcote | 70.6 | 70.0 | 2/9 | 29 |
| seleniumbase-cdp-chrome | 70.3 | 80.0 | 2/9 | 39 |
| cloakbrowser | 70.3 | 50.0 | 0/9 | 9 |
| nodriver-chrome | 69.7 | 70.0 | 2/9 | 31 |
| cloakbrowser_headless | 69.2 | 50.0 | 0/9 | 12 |
| adspower_headless | 67.5 | 60.0 | 1/9 | 25 |
| shardbrowser | 64.9 | 60.0 | 1/9 | 30 |
| adspower | 64.4 | 50.0 | 0/9 | 21 |
| shardbrowser_headless | 62.0 | 40.0 | 0/9 | 16 |
| zendriver-chrome_headless | 58.1 | 70.0 | 5/9 | 54 |
| selenium-chrome__no_proxy | 44.1 | 60.0 | 6/9 | 72 |
| tf-playwright-stealth-chromium | 42.2 | 40.0 | 5/9 | 56 |
| tf-playwright-stealth-chromium_headless | 42.2 | 40.0 | 5/9 | 56 |
| playwright-firefox | 36.4 | 60.0 | 9/9 | 87 |
| playwright-firefox_headless | 36.4 | 60.0 | 9/9 | 87 |
| playwright-chrome | 31.5 | 50.0 | 8/9 | 87 |
| tf-playwright-stealth-firefox | 31.1 | 50.0 | 8/9 | 88 |
| tf-playwright-stealth-firefox_headless | 26.1 | 40.0 | 8/9 | 88 |
| pydoll-chrome_headless | 10.1 | 10.0 | 8/9 | 90 |
| selenium-chrome_headless__no_proxy | 8.4 | 10.0 | 9/9 | 93 |
| nodriver-chrome_headless | 6.9 | 0.0 | 8/9 | 86 |
| patchright_headless | 5.1 | 0.0 | 8/9 | 90 |
| playwright-chrome_headless | 0.1 | 0.0 | 9/9 | 100 |


## Bot Detection Tests
✅ looks human · ⚠️ suspicious · ❌ detected as bot · ❔ test didn't finish (not counted)

Risk (0 - human, 100 - bot) is the average over the tests: the site's own score where it has one (CleanTalk: 100 - Human Score, APIVoid: risk score, CreepJS: headless/stealth %, Fingerprint-Scan: bot score), otherwise its verdict (✅ 0, ⚠️ 50, ❌ 100). Engines are sorted by it.

| Engine | cleantalk | scrapfly | browserscan | apivoid | pixelscan | sannysoft | creepjs_headless | deviceandbrowserinfo | fingerprint_scan | Detected by | Risk |
|-----------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|------------:|-----:|
| invisible-playwright_headless | ✅ score 100 | ✅ 14/14 safe | ✅ 17/17 normal | ✅ risk 0 | ✅ 69/69 clear | ✅ 30/30 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 15 | 0/9 | 2 |
| invisible-playwright | ✅ score 100 | ✅ 14/14 safe | ✅ 17/17 normal | ✅ risk 20 | ✅ 69/69 clear | ✅ 30/30 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 15 | 0/9 | 4 |
| cloakbrowser | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ✅ risk 20 | ✅ 92/92 clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 15 | 0/9 | 9 |
| cloakbrowser_headless | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ✅ risk 10 | ✅ 92/92 clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 45 | 0/9 | 12 |
| clearcote_headless | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ⚠️ risk 53 | ✅ 101/101 clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 26 | 0/9 | 14 |
| shardbrowser_headless | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ⚠️ risk 58 | ✅ 91/91 clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 36 | 0/9 | 16 |
| camoufox_headless | ✅ score 100 | ✅ 14/14 safe | ✅ 17/17 normal | ⚠️ risk 50 | ✅ 69/69 clear | ⚠️ 1 warn | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 57 | 0/9 | 17 |
| camoufox | ✅ score 100 | ✅ 14/14 safe | ✅ 17/17 normal | ⚠️ risk 40 | ✅ 69/69 clear | ⚠️ 1 warn | ✅ headless 0%, stealth 0% | ✅ human | ❌ bot score 92 | 1/9 | 20 |
| adspower | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ⚠️ risk 60 | ✅ 102/102 clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 81 | 0/9 | 21 |
| adspower_headless | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ❌ risk 75 | ✅ 102/102 clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 100 | 1/9 | 25 |
| zendriver-chrome | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ⚠️ risk 36 | ✅ 90/90 clear | ❌ 2 failed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 69 | 1/9 | 28 |
| clearcote | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ✅ risk 33 | ✅ 101/101 clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ❌ bot, 1 signal | ❌ bot score 76 | 2/9 | 29 |
| shardbrowser | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ⚠️ risk 55 | ✅ 91/91 clear | ❌ 2 failed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 66 | 1/9 | 30 |
| patchright | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ✅ risk 26 | ✅ 90/90 clear | ❌ 2 failed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 99 | 1/9 | 31 |
| nodriver-chrome | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ✅ risk 26 | ✅ 90/90 clear | ❌ 2 failed | ✅ headless 0%, stealth 0% | ✅ human | ❌ bot score 100 | 2/9 | 31 |
| pydoll-chrome | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ⚠️ risk 41 | ✅ 90/90 clear | ❌ 2 failed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 99 | 1/9 | 32 |
| seleniumbase-cdp-chrome | ✅ score 100 | ⚠️ 1 suspicious | ✅ 17/17 normal | ⚠️ risk 36 | ❌ 1 not clear | ❌ 2 failed | ✅ headless 0%, stealth 0% | ✅ human | ⚠️ bot score 69 | 2/9 | 39 |
| zendriver-chrome_headless | ✅ score 84 | ⚠️ 1 suspicious | ✅ 17/17 normal | ❌ risk 85 | ✅ 90/90 clear | ❌ 1 failed | ❌ headless 33%, stealth 0% | ❌ bot, 1 signal | ❌ bot score 100 | 5/9 | 54 |
| tf-playwright-stealth-chromium | ✅ score 100 | ✅ 14/14 safe | ❌ robot | ❌ risk 100 | ❌ 3 not clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ❌ bot, 4 signals | ❌ bot score 100 | 5/9 | 56 |
| tf-playwright-stealth-chromium_headless | ✅ score 100 | ✅ 14/14 safe | ❌ robot | ❌ risk 100 | ❌ 3 not clear | ✅ 31/31 passed | ✅ headless 0%, stealth 0% | ❌ bot, 4 signals | ❌ bot score 100 | 5/9 | 56 |
| selenium-chrome__no_proxy | ⚠️ score 70 | ⚠️ 1 suspicious | ❌ robot, Selenium | ❌ risk 66 | ❌ 1 not clear | ❌ 2 failed | ✅ headless 0%, stealth 0% | ❌ bot, 2 signals | ❌ bot score 100 | 6/9 | 72 |
| nodriver-chrome_headless | ⚠️ score 58 | ❌ 1 detected | ❌ robot | ❌ blocked (403) | ❌ 2 not clear | ❌ 4 failed | ❌ headless 33%, stealth 0% | ❌ bot, 2 signals | ❌ bot score 100 | 8/9 | 86 |
| playwright-chrome | ⚠️ score 50 | ❌ 1 detected | ❌ robot, WebDriver | ❌ risk 100 | ❌ 2 not clear | ❌ 2 failed | ❌ headless 33%, stealth 0% | ❌ bot, 6 signals | ❌ bot score 100 | 8/9 | 87 |
| playwright-firefox | ❌ score 41 | ❌ 1 detected | ❌ robot, WebDriver | ❌ risk 93 | ❌ 2 not clear | ❌ 3 failed | ❌ headless 33%, stealth 0% | ❌ bot, 2 signals | ❌ bot score 100 | 9/9 | 87 |
| playwright-firefox_headless | ❌ score 41 | ❌ 1 detected | ❌ robot, WebDriver | ❌ risk 93 | ❌ 2 not clear | ❌ 3 failed | ❌ headless 33%, stealth 0% | ❌ bot, 2 signals | ❌ bot score 100 | 9/9 | 87 |
| tf-playwright-stealth-firefox | ⚠️ score 50 | ❌ 1 detected | ❌ robot, WebDriver | ❌ risk 100 | ❌ 3 not clear | ❌ 4 failed | ❌ headless 33%, stealth 40% | ❌ bot, 3 signals | ❌ bot score 100 | 8/9 | 88 |
| tf-playwright-stealth-firefox_headless | ⚠️ score 50 | ❌ 1 detected | ❌ robot, WebDriver | ❌ risk 100 | ❌ 3 not clear | ❌ 4 failed | ❌ headless 33%, stealth 40% | ❌ bot, 3 signals | ❌ bot score 100 | 8/9 | 88 |
| patchright_headless | ⚠️ score 58 | ❌ 1 detected | ❌ robot | ❌ blocked (403) | ❌ 2 not clear | ❌ 4 failed | ❌ headless 67%, stealth 0% | ❌ bot, 2 signals | ❌ bot score 100 | 8/9 | 90 |
| pydoll-chrome_headless | ⚠️ score 58 | ❌ 1 detected | ❌ robot | ❌ blocked (403) | ❌ 2 not clear | ❌ 4 failed | ❌ headless 67%, stealth 0% | ❌ bot, 2 signals | ❌ bot score 100 | 8/9 | 90 |
| selenium-chrome_headless__no_proxy | ❌ score 28 | ❌ 1 detected | ❌ robot, Selenium | ❌ blocked (403) | ❌ 3 not clear | ❌ 4 failed | ❌ headless 67%, stealth 0% | ❌ bot, 5 signals | ❌ bot score 100 | 9/9 | 93 |
| playwright-chrome_headless | ❌ score 1 | ❌ 2 detected | ❌ robot, WebDriver | ❌ blocked (403) | ❌ 6 not clear | ❌ 12 failed | ❌ headless 100%, stealth 0% | ❌ bot, 6 signals | ❌ bot score 100 | 9/9 | 100 |

Note: The headed Chromium-based engines ran on a server without a GPU, so they have no WebGL - this is what Sannysoft flags ("WebGL Vendor/Renderer failed"). Headless engines get a software WebGL renderer instead.


## Resource Usage Comparison
| Engine | Memory Usage (MB) | CPU Usage (%) |
|-----------------|------------------:|--------------:|
| adspower | 150.0 | 2.2 |
| adspower_headless | 170.0 | 3.5 |
| tf-playwright-stealth-chromium_headless | 589.0 | 5.2 |
| playwright-chrome_headless | 600.0 | 1.3 |
| playwright-firefox_headless | 933.0 | 31.0 |
| tf-playwright-stealth-chromium | 967.0 | 12.9 |
| pydoll-chrome_headless | 972.0 | 4.1 |
| cloakbrowser_headless | 975.0 | 16.4 |
| playwright-firefox | 978.0 | 23.6 |
| invisible-playwright | 983.0 | 41.3 |
| selenium-chrome_headless__no_proxy | 1013.0 | 4.1 |
| zendriver-chrome_headless | 1037.0 | 17.0 |
| playwright-chrome | 1083.0 | 10.6 |
| cloakbrowser | 1084.0 | 20.6 |
| zendriver-chrome | 1097.0 | 15.3 |
| pydoll-chrome | 1099.0 | 18.7 |
| selenium-chrome__no_proxy | 1123.0 | 14.9 |
| invisible-playwright_headless | 1135.0 | 44.7 |
| seleniumbase-cdp-chrome | 1135.0 | 28.2 |
| tf-playwright-stealth-firefox_headless | 1202.0 | 29.9 |
| clearcote | 1221.0 | 45.4 |
| clearcote_headless | 1285.0 | 85.2 |
| nodriver-chrome_headless | 1320.0 | 3.8 |
| tf-playwright-stealth-firefox | 1414.0 | 43.7 |
| shardbrowser_headless | 1472.0 | 13.8 |
| nodriver-chrome | 1504.0 | 17.9 |
| patchright_headless | 1508.0 | 4.2 |
| shardbrowser | 1544.0 | 23.5 |
| camoufox | 1545.0 | 79.9 |
| camoufox_headless | 1608.0 | 59.1 |
| patchright | 1652.0 | 20.8 |


### Recaptcha Scores - https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php
| Engine | Recaptcha Score (0-1) |
|-----------------|--------------------:|
| adspower | 0.90 |
| adspower_headless | 0.90 |
| camoufox | 0.90 |
| camoufox_headless | 0.90 |
| clearcote | 0.90 |
| clearcote_headless | 0.90 |
| cloakbrowser | 0.90 |
| cloakbrowser_headless | 0.90 |
| invisible-playwright | 0.90 |
| invisible-playwright_headless | 0.90 |
| nodriver-chrome | 0.90 |
| nodriver-chrome_headless | 0.90 |
| patchright | 0.90 |
| patchright_headless | 0.90 |
| playwright-firefox | 0.90 |
| playwright-firefox_headless | 0.90 |
| pydoll-chrome | 0.90 |
| pydoll-chrome_headless | 0.90 |
| selenium-chrome__no_proxy | 0.90 |
| selenium-chrome_headless__no_proxy | 0.90 |
| seleniumbase-cdp-chrome | 0.90 |
| shardbrowser | 0.90 |
| shardbrowser_headless | 0.90 |
| tf-playwright-stealth-firefox | 0.90 |
| tf-playwright-stealth-firefox_headless | 0.90 |
| zendriver-chrome | 0.90 |
| zendriver-chrome_headless | 0.90 |
| playwright-chrome | nan |
| playwright-chrome_headless | nan |
| tf-playwright-stealth-chromium | nan |
| tf-playwright-stealth-chromium_headless | nan |

Note 1: "nan" indicates no score was obtained - the website just stopped working when tests were run

Note 2: `
This Score is taken by solving the reCAPTCHA v3 on your browser.
The Score shows if Google considers you as HUMAN or BOT.
1.0 is very likely a good interaction, 0.0 is very likely a bot
With low score values (< 0.3) you'll get a slow reCAPTCHA 2, it would be hard to solve it.
And vise versa, with score >= 0.7 it will be much easier. 
`


### WebRTC IP (CreepJS) - https://abrahamjuliot.github.io/creepjs
| Engine | WebRTC IP |
|-----------------|----------:|
| adspower | 97.189.111.154 |
| adspower_headless | 172.56.219.96 |
| camoufox | 172.56.153.41 |
| camoufox_headless | 69.112.50.25 |
| clearcote | 107.12.52.229 |
| clearcote_headless | 70.130.166.136 |
| cloakbrowser | 172.4.209.245 |
| cloakbrowser_headless | 68.58.217.217 |
| invisible-playwright | Not detected |
| invisible-playwright_headless | Not detected |
| nodriver-chrome | REAL_IP |
| nodriver-chrome_headless | REAL_IP |
| patchright | REAL_IP |
| patchright_headless | REAL_IP |
| playwright-chrome | REAL_IP |
| playwright-chrome_headless | REAL_IP |
| playwright-firefox | REAL_IP |
| playwright-firefox_headless | REAL_IP |
| pydoll-chrome | REAL_IP |
| pydoll-chrome_headless | REAL_IP |
| selenium-chrome__no_proxy | REAL_IP |
| selenium-chrome_headless__no_proxy | REAL_IP |
| seleniumbase-cdp-chrome | Not detected |
| shardbrowser | Not detected |
| shardbrowser_headless | Not detected |
| tf-playwright-stealth-chromium | REAL_IP |
| tf-playwright-stealth-chromium_headless | REAL_IP |
| tf-playwright-stealth-firefox | REAL_IP |
| tf-playwright-stealth-firefox_headless | REAL_IP |
| zendriver-chrome | Not detected |
| zendriver-chrome_headless | Not detected |

Note: If the WebRTC IP is different from your real IP - no leakage (applicable only with proxy). "Not detected" means WebRTC is blocked.


### IP (Ipify)
| Engine | IP |
|-----------------|----------:|
| adspower | 107.195.49.21 |
| adspower_headless | 75.247.146.166 |
| camoufox | 108.217.179.151 |
| camoufox_headless | 69.112.50.25 |
| clearcote | 107.12.52.229 |
| clearcote_headless | 70.130.166.136 |
| cloakbrowser | 172.4.209.245 |
| cloakbrowser_headless | 75.224.223.158 |
| invisible-playwright | 64.135.135.152 |
| invisible-playwright_headless | 96.245.65.169 |
| nodriver-chrome | 141.126.220.102 |
| nodriver-chrome_headless | 66.117.131.179 |
| patchright | 67.174.234.74 |
| patchright_headless | 98.52.109.165 |
| playwright-chrome | 216.223.223.39 |
| playwright-chrome_headless | 67.197.51.143 |
| playwright-firefox | 173.71.77.12 |
| playwright-firefox_headless | 98.252.228.14 |
| pydoll-chrome | 71.143.207.203 |
| pydoll-chrome_headless | 98.50.251.99 |
| selenium-chrome__no_proxy | REAL_IP |
| selenium-chrome_headless__no_proxy | REAL_IP |
| seleniumbase-cdp-chrome | 108.236.48.229 |
| shardbrowser | 47.177.13.39 |
| shardbrowser_headless | 108.70.80.243 |
| tf-playwright-stealth-chromium | 68.97.88.186 |
| tf-playwright-stealth-chromium_headless | 99.170.234.92 |
| tf-playwright-stealth-firefox | 73.13.114.239 |
| tf-playwright-stealth-firefox_headless | 82.40.110.136 |
| zendriver-chrome | 24.239.63.50 |
| zendriver-chrome_headless | 96.59.44.43 |

Note: If the IP is your proxy's IP - good, your real IP - bad (applicapable only with proxy).

### Visual Dashboard
![Bypass Dashboard](results/example/media/bypass_dashboard.png)

### Recaptcha Score Visualization
![Recaptcha Scores](results/example/media/recaptcha_scores.png)

### Bot Detection Visualization
![Bot Detection Tests](results/example/media/detection_tests.png)

## 🛠️ Installation

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/techinz/browsers-benchmark.git
   cd browsers-benchmark
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install browser engines**

   **Playwright**
   ```bash
   playwright install
   # On Linux also run:
   playwright install-deps
   ```

   **Camoufox**
   ```bash
   # Windows
   camoufox fetch
   
   # Linux  
   python -m camoufox fetch
   sudo apt install -y libgtk-3-0 libx11-xcb1 libasound2
   ```

   **Patchright**
   ```bash
   patchright install chromium
   ```

   **AdsPower** *(optional)*  
   1. Download and install [AdsPower](https://www.adspower.com/download) desktop app
   2. Open AdsPower, go to **Settings → API** and enable the local API
   3. Copy your API key and set `ADSPOWER_API_KEY` in `.env`
   4. Keep AdsPower running while the benchmark is active - it manages the browser process

4. **Configure settings**
   ```bash
   cp .env.example .env
   # Edit .env with your proxy settings if needed
   ```

5. **Configure proxies**
   1. Create a file named `proxies.txt` in the `documents` directory.
   2. Add your proxy URLs in format `http://username:password@proxy_host:port` or `http://proxy_host:port`.  
      ❗️ IMPORTANT (1): Number of proxies has to be not less than number of engines you want to test.  
      ❗️ IMPORTANT (2): Some engines support different proxy protocols - for example, Playwright supports only HTTP and HTTPS, but NoDriver supports only SOCKS5.  
         This implies that you have to add multiple proxy protocols to the `proxies.txt` file or exclude some engines from the test.  
         At the moment you need all HTTP/HTTPS proxies and at least 1 SOCKS5 for NoDriver. Also, the benchmark will show you what proxy protocols are missing.  
      ❗️ IMPORTANT (3): Selenium won't use any proxies.  

   Example `proxies.txt` content (each line is a separate proxy):
   ```
   http://proxy1.example.com:8080
   http://proxy2.example.com:8080
   http://username:password@proxy3.example.com:8080
   http://username:password@proxy4.example.com:8080
   socks5://username:password@proxy5.example.com:8080
   ```

6. **Run benchmark**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Proxy Configuration (highly recommended to enable)
PROXY_ENABLED=true
PROXY_FILE_PATH=documents/proxies.txt
PROXY_MAX_RETRIES=3

# Performance Settings
PAGE_LOAD_TIMEOUT_S=90
PAGE_STABILIZATION_DELAY_S=5
MAX_RETRIES=3

# AdsPower (optional — only needed if running the adspower engine)
# Get your API key from AdsPower desktop app: Settings → API
ADSPOWER_API_KEY=your_api_key_here
ADSPOWER_BASE_URL=http://local.adspower.net:50325
ADSPOWER_GROUP_ID=
```

## 📈 Output & Reports

The benchmark generates reports in the `results/` directory:

- **`summary.md`** - Human-readable markdown report
- **`benchmark_results.json`** - Raw data for further analysis  
- **`media/`** - Generated visualizations and screenshots
  - `bypass_dashboard.png` - Multi-metric dashboard
  - `recaptcha_scores.png` - reCAPTCHA performance chart
  - `detection_tests.png` - Bot detection test verdicts for every engine
  - `screenshots` - Screenshots of all tested targets

Your machine's real IP is detected at startup and saved as `REAL_IP` in the results and on screenshots (page text is masked right before each screenshot), so reports can be shared safely. Text inside cross-origin iframes can't be masked.

## 🏗️ Architecture

The codebase follows a modular architecture for extensibility:

```
├── config/           # Configuration management
├── engines/          # Browser engine implementations  
├── utils/
│   ├── targets/      # Test target definitions
│   ├── report/       # Report generation system
│   ├── logging/      # Structured logging
│   └── ...
└── results/          # Output directory
```

### Adding New Targets
1. Modify `config/benchmark_targets.py` to add custom test targets:

    ```python
    Target(
        name="custom_site",
        url="https://example.com",
        check_function="check_custom_bypass",
        description="Custom site protection test"
    )
    ```
2. Create a check function for the target in `utils/targets/check_bypass`, for example in a file named `custom_bypass.py`:
    ```python
    from engines.base import BrowserEngine

    async def check_custom_bypass(engine: BrowserEngine) -> bool:
        element_found, element_html = await engine.locator('//div[@class="captcha"]')

        return not element_found # no captcha found - success!
    ```
3. Add it to the checkers mapping in `config/benchmark_targets.py`'s `BypassTargetsSettings`:
    ```python
    checkers: Dict[str, Callable] = Field(
        default_factory=lambda: {
            "check_cloudflare_bypass": check_cloudflare_bypass,
            "check_datadome_bypass": check_datadome_bypass,
            ...
            "check_custom_bypass": check_custom_bypass,
        }
    )
    ```

### Adding New Bot Detection Tests
1. Create a check function in `utils/targets/detection` that reads the site's own verdict and returns it with `detection()`:
    ```python
    from engines.base import BrowserEngine
    from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, detection, wait_for

    RESULT_SCRIPT = "const el = document.querySelector('#score'); return JSON.stringify(el ? parseInt(el.textContent) : null);"

    async def check_custom_detection(engine: BrowserEngine) -> dict:
        score = await wait_for(engine, RESULT_SCRIPT, timeout_s=45)
        if score is None:
            raise Exception("Result not found")

        verdict = HUMAN if score < 30 else SUSPICIOUS if score < 70 else BOT
        return detection(verdict, f"bot score {score}", risk=score, score=score)
    ```
2. Add a `Target` and the function to `DetectionTargetsSettings` in `config/benchmark_targets.py`.

### Adding New Engines
1. Extend the `BrowserEngine` base class:

   ```python  
   class CustomEngine(BrowserEngine):
       async def start(self) -> None:
           # Initialize browser
           
       async def navigate(self, url: str) -> Dict[str, Any]:
           # Navigation logic
   ```
   
   Or, if Playwright-based, extend `PlaywrightBase` base class:
   ```python  
   class CustomPlaywrightBasedEngine(PlaywrightBase):
       ...
   ```
   
    Or, if Selenium-based, extend `SeleniumBase` base class:
   ```python  
   class CustomSeleniumBasedEngine(SeleniumBase):
       ...
   ```
   
2. Add it to the engines mapping in `config/engines.py`'s `EnginesSettings`:
    ```python
    base_engines = [
            {
                "class": PlaywrightEngine,
                "params": {"headless": True, "name": "playwright-chrome_headless", "browser_type": "chromium"}
            },
            ...
            {
                "class": CustomEngine,
                "params": {"headless": True, "name": "custom_engine", "browser_type": "chromium"}
            }
   ]
    ```

## 🔧 Platform-Specific Notes
### Troubleshooting

**Common Issues:**
- **Detection failures**: Verify proxy configuration and target accessibility

## 🤝 Contributing

Contributions are welcome! Areas where help is needed:
- **New Protection Systems**: Add support for additional bot detection services
- **Browser Engines**: Implement support for new automation frameworks (e.g. Selenium-based)
- **Analysis Tools**: Enhance reporting and visualization

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer
This tool is designed for educational and research purposes. Users are responsible for ensuring compliance with website terms of service and applicable laws. The authors and contributors do not encourage or endorse any malicious use of this software.