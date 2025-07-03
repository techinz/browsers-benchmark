# Browser Engine Benchmark

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A toolkit for testing browser automation engines against modern web protection systems. It checks how well each engine can bypass bot detection and measures their speed, resource usage, and resistance to fingerprinting.

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
- <i>More engines coming soon</i>

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
<i>Real IP in this example - 193.32.248.250</i>  
<i>Proxy IP in this example is different for each engine</i>

### Overall Bypass Rate
| Engine | Bypass Rate (%) |
|-----------------|----------------:|
| camoufox | 100.0 |
| camoufox_headless | 100.0 |
| playwright-firefox_headless | 66.7 |
| playwright-firefox | 50.0 |
| tf-playwright-stealth-firefox_headless | 50.0 |
| tf-playwright-stealth-chromium_headless | 50.0 |
| patchright_headless | 33.3 |
| patchright | 33.3 |
| playwright-chrome | 33.3 |
| playwright-chrome_headless | 33.3 |
| tf-playwright-stealth-firefox | 33.3 |
| tf-playwright-stealth-chromium | 16.7 |


### Resource Usage Comparison
| Engine | Memory Usage (MB) | CPU Usage (%) |
|-----------------|------------------:|--------------:|
| playwright-chrome_headless | 213.0 | 5.2 |
| tf-playwright-stealth-chromium_headless | 320.0 | 0.0 |
| tf-playwright-stealth-chromium | 387.0 | 6.2 |
| playwright-chrome | 409.0 | 0.0 |
| patchright | 532.0 | 72.4 |
| patchright_headless | 546.0 | 0.0 |
| tf-playwright-stealth-firefox | 609.0 | 15.5 |
| tf-playwright-stealth-firefox_headless | 804.0 | 5.2 |
| playwright-firefox_headless | 869.0 | 10.3 |
| playwright-firefox | 944.0 | 25.8 |
| camoufox | 971.0 | 0.0 |
| camoufox_headless | 1069.0 | 62.2 |

If the CPU usage is 0 - failed to measure or it really is 0 for CDP sessions. The problem is known and will be fixed.

### Recaptcha Scores - https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php
| Engine | Recaptcha Score (0-1) |
|-----------------|--------------------:|
| camoufox | 0.90 |
| camoufox_headless | 0.90 |
| patchright | 0.90 |
| patchright_headless | 0.90 |
| playwright-chrome | 0.90 |
| playwright-chrome_headless | 0.90 |
| playwright-firefox | 0.90 |
| playwright-firefox_headless | 0.90 |
| tf-playwright-stealth-chromium | 0.90 |
| tf-playwright-stealth-chromium_headless | 0.90 |
| tf-playwright-stealth-firefox | 0.90 |
| tf-playwright-stealth-firefox_headless | 0.90 |

`
This Score is taken by solving the reCAPTCHA v3 on your browser.
The Score shows if Google considers you as HUMAN or BOT.
1.0 is very likely a good interaction, 0.0 is very likely a bot
With low score values (< 0.3) you'll get a slow reCAPTCHA 2, it would be hard to solve it.
And vise versa, with score >= 0.7 it will be much easier. 
`


### CreepJS Scores - https://abrahamjuliot.github.io/creepjs
| Engine | Trust Score (%) | Bot Score (%) | WebRTC IP |
|-----------------|----------------:|--------------:|----------:|
| patchright | 93.00 | 0.00 | 193.32.248.250 |
| playwright-firefox_headless | 93.00 | 0.00 | 193.32.248.250 |
| playwright-chrome_headless | 91.50 | 0.00 | 193.32.248.250 |
| playwright-chrome | 84.00 | 0.00 | 193.32.248.250 |
| patchright_headless | 69.00 | 13.00 | 193.32.248.250 |
| playwright-firefox | 69.00 | 13.00 | 193.32.248.250 |
| camoufox | 59.50 | 13.00 | 94.228.149.87 |
| camoufox_headless | 59.50 | 13.00 | 86.144.101.200 |
| tf-playwright-stealth-chromium | 0.00 | 25.00 | 193.32.248.250 |
| tf-playwright-stealth-chromium_headless | 0.00 | 25.00 | 193.32.248.250 |
| tf-playwright-stealth-firefox | 0.00 | 25.00 | 193.32.248.250 |
| tf-playwright-stealth-firefox_headless | 0.00 | 25.00 | 193.32.248.250 |

Applicapable only with proxy.
If the WebRTC IP is different from your real IP - no leakage


### IP (Ipify)
| Engine | IP |
|-----------------|----------:|
| camoufox | 94.228.149.87 |
| camoufox_headless | 86.144.101.200 |
| patchright | 190.175.103.65 |
| patchright_headless | 80.41.23.87 |
| playwright-chrome | 184.79.206.236 |
| playwright-chrome_headless | 176.121.229.86 |
| playwright-firefox | 184.79.58.77 |
| playwright-firefox_headless | 181.118.50.213 |
| tf-playwright-stealth-chromium | 184.77.82.82 |
| tf-playwright-stealth-chromium_headless | 70.172.154.65 |
| tf-playwright-stealth-firefox | 152.59.146.124 |
| tf-playwright-stealth-firefox_headless | 88.213.200.180 |

Applicapable only with proxy.
If the IP is your proxy's IP - good, your real IP - bad.

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
   2. Add your proxy URLs in format `http://username:password@proxy_host:port` or `http://proxy_host:port`. Number of proxies has to be not less than number of engines you want to test.
      
   Example `proxies.txt` content (each line is a separate proxy):
   ```
   http://proxy1.example.com:8080
   http://proxy2.example.com:8080
   http://username:password@proxy3.example.com:8080
   http://username:password@proxy4.example.com:8080
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
PAGE_LOAD_TIMEOUT_MS=90000
PAGE_STABILIZATION_DELAY_S=5
MAX_RETRIES=3
```

## 📈 Output & Reports

The benchmark generates reports in the `results/` directory:

- **`summary.md`** - Human-readable markdown report
- **`benchmark_results_*.json`** - Raw data for further analysis  
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