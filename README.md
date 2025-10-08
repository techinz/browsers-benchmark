# Browser Engine Benchmark

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A toolkit for testing browser automation engines against modern web protection systems. It checks how well each engine can bypass bot detection and measures their speed, resource usage, and resistance to fingerprinting.

---

<p align="center">
    <a href="https://www.nstproxy.com/?type=flow&utm_source=techinz" target="_blank">
        <img width="624" height="277" alt="Image" src="https://github.com/user-attachments/assets/280e27fd-90c6-4bc3-8300-ab3ed16e57f7" />
    </a>
</p>

If you're looking for a reliable proxy to <b>bypass anti-bot systems, scrape at scale, and access geo-restricted data without blocks</b>, <a href="https://www.nstproxy.com/?type=flow&utm_source=techinz">Nstproxy</a> is built for you. Perfect for large-scale web scraping, SEO monitoring, e-commerce data collection, price intelligence, and automation — even under the strictest anti-scraping protections.

Nstproxy offers a global pool of residential, datacenter, and IPv6 proxies with rotating or sticky sessions, advanced anti-block tech, and pricing from $0.1/GB for maximum uptime and ROI.

<b>Key Features:</b>
- 🌍 <b>Global IP Coverage</b> – 110M+ residential IPs, 195+ countries, IPv4/IPv6
- 🔄 <b>Rotation Control</b> – Per request or sticky sessions for consistent sessions
- 🛡 <b>Anti-ban & CAPTCHA Bypass</b> – Designed for high scraping success rates
- 💰 <b>Affordable</b> – From $0.1/GB, far below market average
- ⚡ <b>Multi-purpose</b> – Scraping, SEO, automation, e-commerce, analytics
- 🔌 <b>Easy Integration</b> – Python, Puppeteer, Playwright, Node.js
- 📈 <b>Unlimited Scaling</b> – Handle any volume with stable performance

An all-in-one proxy solution for developers and traders who need reliability, scalability, and cost efficiency.  
👉 Learn more: <a href="https://www.nstproxy.com/?type=flow&utm_source=techinz">Nstproxy.com</a>: https://www.nstproxy.com/?type=flow&utm_source=techinz  | <a href="https://app.nstproxy.com/?utm_source=techinz">Dashboard</a>  
Telegram: https://t.me/nstproxy Discord: https://discord.gg/5jjWCAmvng   
Use code: <b>TECHINZ get 10% OFF</b>

---

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
- <i>More systems coming soon</i>

### Browser Engine Support
- <a href="https://playwright.dev">**Playwright**</a> - Microsoft's automation framework (Chrome, Firefox, Safari)
- <a href="https://camoufox.com">**Camoufox**</a> - Playwright-based
- <a href="https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python">**Patchright**</a> - Playwright-based
- <a href="https://github.com/tinyfish-io/tf-playwright-stealth">**Playwright Stealth**</a> - Playwright-based
- <a href="https://www.selenium.dev">**Selenium**</a> - Open-source browser automation framework (apparently deprecated, so it is tested without proxies)
- <a href="https://seleniumbase.io/">**Seleniumbase**</a> - Open-source professional toolkit for web automation activities
- <a href="https://github.com/ultrafunkamsterdam/nodriver">**NoDriver**</a> - Open-source browser automation framework (supports only SOCKS5 proxies)
- <a href="https://github.com/cdpdriver/zendriver">**ZenDriver**</a> - NoDriver-based
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

## 📊 Sample Results
This benchmark provides detailed comparative analysis. Here's an excerpt from a recent test run (more in <a href="results/example">results/example</a>):  
<i>Real IP in this example - 149.102.240.75</i>  
<i>Proxy IP in this example is different for each engine</i>

### Overall Bypass Rate
| Engine | Bypass Rate (%) |
|-----------------|----------------:|
| camoufox_headless | 83.3 |
| nodriver-chrome | 83.3 |
| playwright-firefox | 83.3 |
| camoufox | 66.7 |
| patchright | 66.7 |
| playwright-firefox_headless | 66.7 |
| zendriver-chrome_headless | 50.0 |
| tf-playwright-stealth-firefox_headless | 50.0 |
| tf-playwright-stealth-chromium_headless | 50.0 |
| tf-playwright-stealth-chromium | 50.0 |
| seleniumbase-cdp-chrome | 50.0 |
| nodriver-chrome_headless | 33.3 |
| tf-playwright-stealth-firefox | 33.3 |
| selenium-chrome__no_proxy | 33.3 |
| playwright-chrome_headless | 33.3 |
| zendriver-chrome | 33.3 |
| playwright-chrome | 16.7 |
| patchright_headless | 16.7 |
| selenium-chrome_headless__no_proxy | 16.7 |


### Resource Usage Comparison
| Engine | Memory Usage (MB) | CPU Usage (%) |
|-----------------|------------------:|--------------:|
| playwright-chrome_headless | 212.0 | 4.9 |
| tf-playwright-stealth-chromium_headless | 298.0 | 9.4 |
| selenium-chrome_headless__no_proxy | 354.0 | 11.5 |
| zendriver-chrome | 364.0 | 10.2 |
| seleniumbase-cdp-chrome | 375.0 | 14.0 |
| zendriver-chrome_headless | 424.0 | 13.4 |
| playwright-chrome | 454.0 | 20.2 |
| tf-playwright-stealth-chromium | 462.0 | 19.8 |
| selenium-chrome__no_proxy | 519.0 | 15.5 |
| nodriver-chrome_headless | 547.0 | 20.0 |
| nodriver-chrome | 554.0 | 19.0 |
| patchright_headless | 560.0 | 12.6 |
| playwright-firefox_headless | 606.0 | 28.1 |
| tf-playwright-stealth-firefox | 659.0 | 26.4 |
| patchright | 709.0 | 19.2 |
| tf-playwright-stealth-firefox_headless | 822.0 | 46.2 |
| camoufox | 1007.0 | 43.5 |
| playwright-firefox | 1012.0 | 51.7 |
| camoufox_headless | 1037.0 | 45.5 |


### Recaptcha Scores - https://antcpt.com/score_detector
| Engine | Recaptcha Score (0-1) |
|-----------------|--------------------:|
| patchright | 0.30 |
| camoufox | 0.10 |
| camoufox_headless | 0.10 |
| patchright_headless | 0.10 |
| playwright-chrome | 0.10 |
| playwright-firefox | 0.10 |
| playwright-firefox_headless | 0.10 |
| seleniumbase-cdp-chrome | 0.10 |
| tf-playwright-stealth-chromium | 0.10 |
| tf-playwright-stealth-chromium_headless | 0.10 |
| tf-playwright-stealth-firefox | 0.10 |
| tf-playwright-stealth-firefox_headless | 0.10 |
| nodriver-chrome | nan |
| nodriver-chrome_headless | nan |
| playwright-chrome_headless | nan |
| selenium-chrome__no_proxy | nan |
| selenium-chrome_headless__no_proxy | nan |
| zendriver-chrome | nan |
| zendriver-chrome_headless | nan |

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
| camoufox | 0.00 | 0.00 | 179.60.189.65 |
| nodriver-chrome | 0.00 | 0.00 | 149.102.240.75 |
| nodriver-chrome_headless | 0.00 | 0.00 | 149.102.240.75 |
| patchright | 0.00 | 0.00 | 149.102.240.75 |
| patchright_headless | 0.00 | 0.00 | 149.102.240.75 |
| playwright-chrome | 0.00 | 0.00 | 149.102.240.75 |
| playwright-chrome_headless | 0.00 | 0.00 | 149.102.240.75 |
| playwright-firefox | 0.00 | 0.00 | 149.102.240.75 |
| playwright-firefox_headless | 0.00 | 0.00 | 149.102.240.75 |
| selenium-chrome__no_proxy | 0.00 | 0.00 | 149.102.240.75 |
| selenium-chrome_headless__no_proxy | 0.00 | 0.00 | 149.102.240.75 |
| seleniumbase-cdp-chrome | 0.00 | 0.00 | 149.102.240.75 |
| tf-playwright-stealth-chromium | 0.00 | 0.00 | 149.102.240.75 |
| tf-playwright-stealth-chromium_headless | 0.00 | 0.00 | 149.102.240.75 |
| tf-playwright-stealth-firefox | 0.00 | 0.00 | 149.102.240.75 |
| tf-playwright-stealth-firefox_headless | 0.00 | 0.00 |  |
| zendriver-chrome | 0.00 | 0.00 | 149.102.240.75 |
| zendriver-chrome_headless | 0.00 | 0.00 | 149.102.240.75 |
| camoufox_headless | nan | nan | Not detected |

Note: 
1. CreepJS disabled trust and bot scores for now - https://github.com/abrahamjuliot/creepjs/issues/292
2. If the WebRTC IP is different from your real IP - no leakage (applicapable only with proxy).


### IP (Ipify)
| Engine | IP |
|-----------------|----------:|
| camoufox | 179.60.189.65 |
| camoufox_headless | 142.168.221.86 |
| nodriver-chrome | 181.188.19.203 |
| nodriver-chrome_headless | 38.13.154.130 |
| patchright | 73.10.95.50 |
| patchright_headless | 108.153.53.3 |
| playwright-chrome | 31.48.214.36 |
| playwright-chrome_headless | 45.188.194.209 |
| playwright-firefox | 142.168.221.86 |
| playwright-firefox_headless | 165.238.24.218 |
| selenium-chrome__no_proxy | 149.102.240.75 |
| selenium-chrome_headless__no_proxy | 149.102.240.75 |
| seleniumbase-cdp-chrome | 207.146.227.90 |
| tf-playwright-stealth-chromium | 37.5.253.239 |
| tf-playwright-stealth-chromium_headless | 204.204.177.118 |
| tf-playwright-stealth-firefox | 208.32.186.48 |
| tf-playwright-stealth-firefox_headless | 204.205.129.70 |
| zendriver-chrome | 207.146.227.90 |
| zendriver-chrome_headless | 204.205.78.214 |

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