# Browser Engine Benchmark

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A toolkit for testing browser automation engines against modern web protection systems. It checks how well each engine can bypass bot detection and measures their speed, resource usage, and resistance to fingerprinting.

---

<a href="https://www.nstproxy.com/?type=flow&utm_source=techinz" target="_blank">
    <img width="624" height="277" alt="Image" src="https://github.com/user-attachments/assets/36dcd8fe-8127-446a-828b-246d421d9319" />
</a>

If you're looking for a reliable proxy to <b>bypass anti-bot systems, scrape at scale, and access geo-restricted data without blocks</b>, Nstproxy is built for you. Perfect for large-scale web scraping, SEO monitoring, e-commerce data collection, price intelligence, and automation — even under the strictest anti-scraping protections.

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
<i>Real IP in this example - 149.102.240.71</i>  
<i>Proxy IP in this example is different for each engine</i>

### Overall Bypass Rate
| Engine | Bypass Rate (%) |
|-----------------|----------------:|
| camoufox | 83.3 |
| nodriver-chrome | 83.3 |
| patchright | 83.3 |
| camoufox_headless | 66.7 |
| playwright-firefox_headless | 66.7 |
| zendriver-chrome | 66.7 |
| playwright-firefox | 50.0 |
| tf-playwright-stealth-firefox | 50.0 |
| tf-playwright-stealth-chromium_headless | 50.0 |
| playwright-chrome | 50.0 |
| tf-playwright-stealth-firefox_headless | 50.0 |
| zendriver-chrome_headless | 50.0 |
| tf-playwright-stealth-chromium | 50.0 |
| nodriver-chrome_headless | 33.3 |
| playwright-chrome_headless | 33.3 |
| patchright_headless | 33.3 |
| selenium-chrome__no_proxy | 16.7 |
| selenium-chrome_headless__no_proxy | 16.7 |


### Resource Usage Comparison
| Engine | Memory Usage (MB) | CPU Usage (%) |
|-----------------|------------------:|--------------:|
| playwright-chrome_headless | 209.0 | 0.0 |
| tf-playwright-stealth-chromium_headless | 220.0 | 5.2 |
| selenium-chrome_headless__no_proxy | 356.0 | 6.1 |
| zendriver-chrome | 370.0 | 3.3 |
| tf-playwright-stealth-chromium | 410.0 | 15.5 |
| playwright-chrome | 414.0 | 4.4 |
| zendriver-chrome_headless | 437.0 | 6.8 |
| selenium-chrome__no_proxy | 490.0 | 10.0 |
| nodriver-chrome_headless | 508.0 | 7.9 |
| patchright_headless | 545.0 | 0.0 |
| nodriver-chrome | 601.0 | 12.3 |
| tf-playwright-stealth-firefox | 607.0 | 0.0 |
| patchright | 699.0 | 31.1 |
| playwright-firefox_headless | 818.0 | 10.4 |
| tf-playwright-stealth-firefox_headless | 840.0 | 0.0 |
| playwright-firefox | 914.0 | 10.3 |
| camoufox_headless | 958.0 | 0.0 |
| camoufox | 1040.0 | 15.5 |

Note: If the CPU usage is 0 - failed to measure or it really is 0 for CDP sessions. The problem is known and will be fixed.

### Recaptcha Scores - https://antcpt.com/score_detector
| Engine | Recaptcha Score (0-1) |
|-----------------|--------------------:|
| camoufox | 0.30 |
| nodriver-chrome | 0.30 |
| tf-playwright-stealth-firefox | 0.30 |
| nodriver-chrome_headless | 0.30 |
| tf-playwright-stealth-chromium_headless | 0.30 |
| zendriver-chrome_headless | 0.30 |
| selenium-chrome__no_proxy | 0.30 |
| tf-playwright-stealth-firefox_headless | 0.30 |
| camoufox_headless | 0.10 |
| patchright | 0.10 |
| playwright-firefox_headless | 0.10 |
| playwright-firefox | 0.10 |
| playwright-chrome_headless | 0.10 |
| playwright-chrome | 0.10 |
| patchright_headless | 0.10 |
| selenium-chrome_headless__no_proxy | 0.10 |
| tf-playwright-stealth-chromium | 0.10 |
| zendriver-chrome | 0.10 |

Note: `
This Score is taken by solving the reCAPTCHA v3 on your browser.
The Score shows if Google considers you as HUMAN or BOT.
1.0 is very likely a good interaction, 0.0 is very likely a bot
With low score values (< 0.3) you'll get a slow reCAPTCHA 2, it would be hard to solve it.
And vise versa, with score >= 0.7 it will be much easier. 
`


### CreepJS Scores - https://abrahamjuliot.github.io/creepjs
| Engine | Trust Score (%) | Bot Score (%) | WebRTC IP |
|-----------------|----------------:|--------------:|----------:|
| camoufox | 0.00 | 0.00 | 102.0.16.230 |
| camoufox_headless | 0.00 | 0.00 | 93.185.151.247 |
| nodriver-chrome | 0.00 | 0.00 | 149.102.240.71 |
| nodriver-chrome_headless | 0.00 | 0.00 | 149.102.240.71 |
| patchright | 0.00 | 0.00 | 149.102.240.71 |
| patchright_headless | 0.00 | 0.00 | 149.102.240.71 |
| playwright-chrome | 0.00 | 0.00 | 149.102.240.71 |
| playwright-chrome_headless | 0.00 | 0.00 | 149.102.240.71 |
| playwright-firefox | 0.00 | 0.00 | 149.102.240.71 |
| playwright-firefox_headless | 0.00 | 0.00 | 149.102.240.71 |
| selenium-chrome__no_proxy | 0.00 | 0.00 | 149.102.240.71 |
| selenium-chrome_headless__no_proxy | 0.00 | 0.00 | 149.102.240.71 |
| tf-playwright-stealth-chromium | 0.00 | 0.00 | 149.102.240.71 |
| tf-playwright-stealth-chromium_headless | 0.00 | 0.00 | 149.102.240.71 |
| tf-playwright-stealth-firefox | 0.00 | 0.00 | 149.102.240.71 |
| tf-playwright-stealth-firefox_headless | 0.00 | 0.00 | 149.102.240.71 |
| zendriver-chrome | 0.00 | 0.00 | 149.102.240.71 |
| zendriver-chrome_headless | 0.00 | 0.00 | 149.102.240.71 |

Note: 
1. CreepJS disabled trust and bot scores for now - https://github.com/abrahamjuliot/creepjs/issues/292
2. If the WebRTC IP is different from your real IP - no leakage (applicapable only with proxy).


### IP (Ipify)
| Engine | IP |
|-----------------|----------:|
| camoufox | 102.0.16.230 |
| camoufox_headless | 79.3.97.54 |
| nodriver-chrome | 209.35.93.167 |
| nodriver-chrome_headless | 179.43.63.187 |
| patchright | 196.133.10.26 |
| patchright_headless | 189.36.133.109 |
| playwright-chrome | 63.104.232.219 |
| playwright-chrome_headless | 191.81.60.47 |
| playwright-firefox | 185.74.53.51 |
| playwright-firefox_headless | 75.25.150.59 |
| selenium-chrome__no_proxy | 149.102.240.71 |
| selenium-chrome_headless__no_proxy | 149.102.240.71 |
| tf-playwright-stealth-chromium | 98.167.26.122 |
| tf-playwright-stealth-chromium_headless | 92.22.82.4 |
| tf-playwright-stealth-firefox | 189.36.133.109 |
| tf-playwright-stealth-firefox_headless | 77.76.151.73 |
| zendriver-chrome | 103.177.184.213 |
| zendriver-chrome_headless | 181.170.174.42 |

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