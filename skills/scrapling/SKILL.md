---
name: scrapling
description: "Adaptive web scraping framework with anti-bot bypass, spider crawling, and proxy rotation. Use when: extracting data from websites, crawling multiple pages, bypassing Cloudflare/anti-bot, reverse engineering APIs, extracting brand data. NOT for: X/Twitter, login-protected sites, paywalled content."
version: "2.0.0"
metadata:
  {"openclaw":{"emoji":"🕷️","requires":{"bins":["python3"]},"tags":["web-scraping","crawling","research","automation"]}}
---

# Scrapling - Adaptive Web Scraping

## Installation

```bash
pip install "scrapling[all]"
scrapling install
scrapling install camoufox      # Anti-detection browser
playwright install chromium      # For stealth/dynamic mode
pip install cloudscraper         # Cloudflare bypass (optional)
```

> **Note:** Requires Python 3.10+, scrapling v0.4.3+
> **Venv:** Use `~/.openclaw/workspace/scripts/literature_env` (已安装)

## Quick Start

```python
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://example.com')
title = page.css('h1::text').get()
paragraphs = page.css('p::text').getall()
```

## Core Usage

### 1. Basic Fetch
```python
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://example.com')
title = page.css('h1::text').get()
paragraphs = page.css('p::text').getall()
```

### 2. Stealthy Fetch (Anti-Bot / Cloudflare)
```python
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch('https://example.com', headless=True, solve_cloudflare=True)
```

### 3. Dynamic Fetch (Full Browser)
```python
from scrapling.fetchers import DynamicFetcher
page = DynamicFetcher.fetch('https://example.com', headless=True, network_idle=True)
```

### 4. Session Management (v0.3+)
```python
from scrapling.fetchers import FetcherSession, StealthySession, DynamicSession

# Reuse connection with browser impersonation
with FetcherSession(impersonate='chrome') as session:
    page = session.get('https://example.com', stealthy_headers=True)

# Stealthy session (anti-bot)
with StealthySession(headless=True) as session:
    page = session.get('https://protected-site.com')

# Dynamic session (full browser)
with DynamicSession(headless=True) as session:
    page = session.get('https://spa-site.com')
```

### 5. Async Fetchers
```python
from scrapling.fetchers import AsyncFetcher, AsyncStealthySession
import asyncio

async def main():
    page = await AsyncFetcher.get('https://example.com')
    print(page.css('h1::text').get())

asyncio.run(main())
```

### 6. Adaptive Parsing (Survives Site Changes)
```python
items = page.css('.product', auto_save=True)   # First scrape - saves selectors
items = page.css('.product', adaptive=True)     # Later - relocates if site changed
```

### 7. CLI
```bash
scrapling extract get https://example.com output.html
scrapling extract stealthy-fetch https://example.com output.html
scrapling shell https://example.com
```

## Selection Methods
```python
page.css('.quote')                        # CSS selector
page.xpath('//div[@class="quote"]')       # XPath
page.find_all('div', class_='quote')      # BeautifulSoup-style
element.parent                            # Navigate DOM
element.find_similar()                    # Find similar elements
```

## Proxy Rotation
```python
from scrapling import ProxyRotator

rotator = ProxyRotator(["http://proxy1:8080", "http://proxy2:8080"])
page = Fetcher.get(url, proxy_rotator=rotator)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 403/429 Blocked | `StealthyFetcher` or `cloudscraper` |
| Cloudflare | `StealthyFetcher.fetch(..., solve_cloudflare=True)` |
| JavaScript required | `DynamicFetcher` |
| Site changed | Use `adaptive=True` |
| Captcha | Cannot bypass — skip or use official API |
| ModuleNotFoundError | Run `scrapling install` then `scrapling install camoufox` |

## Advanced Topics

For detailed examples, read these reference files as needed:

- **Spider crawling, proxy rotation, sessions** → [references/advanced-examples.md](references/advanced-examples.md)
- **API reverse engineering** → [references/advanced-examples.md#api-reverse-engineering](references/advanced-examples.md)
- **Brand data extraction** → [references/advanced-examples.md#brand-data-extraction](references/advanced-examples.md)
- **Sitemap crawling** → [references/advanced-examples.md#sitemap-crawl](references/advanced-examples.md)

## Credits
- **Library:** https://github.com/D4Vinci/Scrapling (BSD-3-Clause, by D4Vinci)
- **Docs:** https://scrapling.readthedocs.io
- **API RE methodology:** @paoloanzn (https://github.com/paoloanzn/free-solscan-api)
