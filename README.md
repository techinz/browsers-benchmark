# Browser Engine Benchmark

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A toolkit for testing browser automation engines against modern web protection systems. It checks how well each engine can bypass bot detection and measures their speed, resource usage, and resistance to fingerprinting.

<i>(Need some help with <b>Automation</b>? You can  <a href="https://automation.techinz.dev">hire me</a> for custom development or consulting!)</i>

## 🎯 Overview
Modern web applications use advanced bot detection like Cloudflare, DataDome, and Imperva to block automated access. This benchmark suite shows how different browser automation engines handle these defenses:
- **Bypass Success Rate**: Effectiveness against major protection systems
- **Performance Metrics**: Memory usage, CPU consumption, and page load times
- **Fingerprinting Resistance**: reCAPTCHA scores and CreepJS trust ratings
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

### Browser Engine Support
- <a href="https://www.adspower.com">**AdsPower**</a> - <b>(Proprietary)</b> Anti-detect browser with per-profile fingerprinting. Requires AdsPower desktop app running locally and an API key.
- <a href="https://playwright.dev">**Playwright**</a> - <b>(Open-Source)</b> Microsoft's automation framework (Chrome, Firefox, Safari)
- <a href="https://camoufox.com">**Camoufox**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python">**Patchright**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/tinyfish-io/tf-playwright-stealth">**Playwright Stealth**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/CloakHQ/cloakbrowser">**CloakBrowser**</a> - <b>(Open-Source)</b> Playwright-based
- <a href="https://github.com/feder-cr/invisible_playwright">**invisible_playwright**</a> - <b>(Open-Source)</b> Playwright-based, patched Firefox with source-level fingerprint
- <a href="https://github.com/clearcotelabs/clearcote-browser">**Clearcote**</a> - <b>(Open-Source)</b> Playwright-based. Runs the open build without a key; `CLEARCOTE_LICENSE_KEY` switches to the licensed build
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

## Overall Bypass Rate
| Engine | Bypass Rate (%) |
|-----------------|----------------:|
| pydoll-chrome | 90.0 |
| invisible-playwright_headless | 80.0 |
| nodriver-chrome | 80.0 |
| patchright | 80.0 |
| clearcote_headless | 80.0 |
| zendriver-chrome | 80.0 |
| camoufox | 70.0 |
| invisible-playwright | 70.0 |
| adspower | 70.0 |
| selenium-chrome__no_proxy | 70.0 |
| seleniumbase-cdp-chrome | 70.0 |
| adspower_headless | 60.0 |
| clearcote | 60.0 |
| zendriver-chrome_headless | 60.0 |
| tf-playwright-stealth-firefox_headless | 60.0 |
| cloakbrowser | 50.0 |
| camoufox_headless | 50.0 |
| tf-playwright-stealth-chromium | 50.0 |
| cloakbrowser_headless | 50.0 |
| playwright-chrome | 50.0 |
| playwright-firefox | 50.0 |
| playwright-firefox_headless | 50.0 |
| tf-playwright-stealth-firefox | 40.0 |
| tf-playwright-stealth-chromium_headless | 40.0 |
| playwright-chrome_headless | 10.0 |
| selenium-chrome_headless__no_proxy | 10.0 |
| nodriver-chrome_headless | 0.0 |
| pydoll-chrome_headless | 0.0 |
| patchright_headless | 0.0 |


## Resource Usage Comparison
| Engine | Memory Usage (MB) | CPU Usage (%) |
|-----------------|------------------:|--------------:|
| adspower_headless | 158.0 | 3.7 |
| adspower | 185.0 | 3.3 |
| tf-playwright-stealth-chromium_headless | 596.0 | 6.3 |
| playwright-chrome_headless | 626.0 | 3.9 |
| pydoll-chrome_headless | 970.0 | 4.0 |
| invisible-playwright | 971.0 | 34.7 |
| cloakbrowser_headless | 973.0 | 19.4 |
| selenium-chrome_headless__no_proxy | 1017.0 | 5.8 |
| zendriver-chrome_headless | 1026.0 | 13.1 |
| cloakbrowser | 1056.0 | 16.7 |
| invisible-playwright_headless | 1090.0 | 42.6 |
| camoufox | 1092.0 | 28.9 |
| pydoll-chrome | 1103.0 | 22.3 |
| zendriver-chrome | 1108.0 | 23.3 |
| selenium-chrome__no_proxy | 1138.0 | 20.8 |
| seleniumbase-cdp-chrome | 1146.0 | 30.7 |
| tf-playwright-stealth-chromium | 1173.0 | 10.8 |
| playwright-chrome | 1187.0 | 15.9 |
| clearcote | 1203.0 | 62.4 |
| tf-playwright-stealth-firefox | 1253.0 | 37.2 |
| clearcote_headless | 1293.0 | 86.2 |
| nodriver-chrome_headless | 1330.0 | 4.5 |
| tf-playwright-stealth-firefox_headless | 1362.0 | 53.3 |
| playwright-firefox | 1370.0 | 55.9 |
| playwright-firefox_headless | 1373.0 | 58.3 |
| nodriver-chrome | 1429.0 | 18.9 |
| camoufox_headless | 1454.0 | 54.5 |
| patchright_headless | 1481.0 | 3.6 |
| patchright | 1666.0 | 28.5 |


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


### CreepJS Scores - https://abrahamjuliot.github.io/creepjs
| Engine | Trust Score (%) | Bot Score (%) | WebRTC IP |
|-----------------|----------------:|--------------:|----------:|
| adspower | 0.00 | 0.00 | 76.38.23.42 |
| adspower_headless | 0.00 | 0.00 | 96.27.46.243 |
| camoufox | 0.00 | 0.00 | 50.26.201.59 |
| camoufox_headless | 0.00 | 0.00 | 107.136.236.92 |
| clearcote | 0.00 | 0.00 | 162.220.232.51 |
| clearcote_headless | 0.00 | 0.00 | 184.58.65.71 |
| cloakbrowser | 0.00 | 0.00 | 99.129.117.52 |
| cloakbrowser_headless | 0.00 | 0.00 | 76.97.38.119 |
| invisible-playwright | 0.00 | 0.00 |  |
| invisible-playwright_headless | 0.00 | 0.00 |  |
| nodriver-chrome | 0.00 | 0.00 | REAL_IP |
| nodriver-chrome_headless | 0.00 | 0.00 | REAL_IP |
| patchright | 0.00 | 0.00 | REAL_IP |
| patchright_headless | 0.00 | 0.00 | REAL_IP |
| playwright-chrome | 0.00 | 0.00 | REAL_IP |
| playwright-chrome_headless | 0.00 | 0.00 | REAL_IP |
| playwright-firefox | 0.00 | 0.00 | REAL_IP |
| playwright-firefox_headless | 0.00 | 0.00 | REAL_IP |
| pydoll-chrome | 0.00 | 0.00 | REAL_IP |
| pydoll-chrome_headless | 0.00 | 0.00 | REAL_IP |
| selenium-chrome__no_proxy | 0.00 | 0.00 | REAL_IP |
| selenium-chrome_headless__no_proxy | 0.00 | 0.00 | REAL_IP |
| seleniumbase-cdp-chrome | 0.00 | 0.00 |  |
| tf-playwright-stealth-chromium | 0.00 | 0.00 | REAL_IP |
| tf-playwright-stealth-chromium_headless | 0.00 | 0.00 | REAL_IP |
| tf-playwright-stealth-firefox | 0.00 | 0.00 | REAL_IP |
| tf-playwright-stealth-firefox_headless | 0.00 | 0.00 | REAL_IP |
| zendriver-chrome | 0.00 | 0.00 |  |
| zendriver-chrome_headless | 0.00 | 0.00 |  |

Note: 
1. CreepJS disabled trust and bot scores for now - https://github.com/abrahamjuliot/creepjs/issues/292
2. If the WebRTC IP is different from your real IP - no leakage (applicable only with proxy).


### IP (Ipify)
| Engine | IP |
|-----------------|----------:|
| adspower | 67.173.191.76 |
| adspower_headless | 96.27.46.243 |
| camoufox | 50.26.201.59 |
| camoufox_headless | 107.136.236.92 |
| clearcote | 162.220.232.51 |
| clearcote_headless | 173.64.64.227 |
| cloakbrowser | 99.129.117.52 |
| cloakbrowser_headless | 108.206.169.72 |
| invisible-playwright | 74.194.143.108 |
| invisible-playwright_headless | 24.49.49.192 |
| nodriver-chrome | 104.176.174.41 |
| nodriver-chrome_headless | 71.75.40.222 |
| patchright | 68.192.100.74 |
| patchright_headless | 72.200.220.88 |
| playwright-chrome | 73.96.79.106 |
| playwright-chrome_headless | 108.207.76.135 |
| playwright-firefox | 68.54.208.109 |
| playwright-firefox_headless | 72.82.21.32 |
| pydoll-chrome | 68.226.171.120 |
| pydoll-chrome_headless | 23.117.134.46 |
| selenium-chrome__no_proxy | REAL_IP |
| selenium-chrome_headless__no_proxy | REAL_IP |
| seleniumbase-cdp-chrome | 204.111.137.63 |
| tf-playwright-stealth-chromium | 76.117.112.121 |
| tf-playwright-stealth-chromium_headless | 24.192.108.243 |
| tf-playwright-stealth-firefox | 82.40.102.67 |
| tf-playwright-stealth-firefox_headless | 135.26.83.225 |
| zendriver-chrome | 73.16.149.151 |
| zendriver-chrome_headless | 99.68.64.97 |

Note: If the IP is your proxy's IP - good, your real IP - bad (applicapable only with proxy).

### Visual Dashboard
![Bypass Dashboard](results/example/media/bypass_dashboard.png)

### Recaptcha Score Visualization
![Recaptcha Scores](results/example/media/recaptcha_scores.png)

### CreepJS Visualization
![CreepJS Scores](results/example/media/creepjs_scores.png)

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
  - `creepjs_scores.png` - Fingerprinting resistance analysis
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