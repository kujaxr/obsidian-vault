# Advanced Scrapling Examples

## Table of Contents
1. [Spider Crawling Patterns](#spider-crawling-patterns)
2. [Proxy Rotation](#proxy-rotation)
3. [Session Management](#session-management)
4. [API Reverse Engineering](#api-reverse-engineering)
5. [Brand Data Extraction](#brand-data-extraction)
6. [Sitemap Crawl](#sitemap-crawl)

---

## Spider Crawling Patterns

### Basic Spider

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "demo"
    start_urls = ["https://example.com"]
    concurrent_requests = 3
    
    async def parse(self, response: Response):
        for item in response.css('.item'):
            yield {"title": item.css('h2::text').get()}
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])

MySpider().start()
```

### Auto-Crawl Entire Domain

```python
from scrapling.spiders import Spider, Response
from urllib.parse import urljoin

class EasyCrawl(Spider):
    name = "easy_crawl"
    start_urls = ["https://example.com"]
    concurrent_requests = 3
    
    def __init__(self):
        super().__init__()
        self.visited = set()
    
    async def parse(self, response: Response):
        yield {'url': response.url, 'title': response.css('title::text').get()}
        if len(self.visited) >= 50: return
        self.visited.add(response.url)
        for link in response.css('a::attr(href)').getall()[:20]:
            full_url = urljoin(response.url, link)
            if full_url not in self.visited:
                yield response.follow(full_url)

EasyCrawl().start()
```

### Spider with uvloop (Faster Async)

```python
MySpider().start(use_uvloop=True)
```

---

## Proxy Rotation

```python
from scrapling import ProxyRotator

# Thread-safe proxy rotation
rotator = ProxyRotator(["http://proxy1:8080", "http://proxy2:8080"])

# Works with all fetchers
Fetcher.get(url, proxy_rotator=rotator)
StealthyFetcher.fetch(url, proxy_rotator=rotator)
```

---

## Session Management

```python
from scrapling.fetchers import FetcherSession
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import AsyncStealthySession

# Simple session
with FetcherSession(impersonate='chrome') as session:
    page = session.get('https://example.com', stealthy_headers=True)

# Multi-session spider
class MultiSessionSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]
    
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
    
    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            if "protected" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast", callback=self.parse)
```

---

## API Reverse Engineering

> "Web scraping is 80% reverse engineering" — @paoloanzn

### Discovery Steps

1. Open DevTools (F12) → Network tab → filter XHR/Fetch
2. Look for JSON responses from `/api/*` endpoints
3. Check Initiator column → find auth header in JS files
4. Extract token generation logic (search for header name like `Authorization`, `X-API-Key`)
5. Replicate in Python

### Cloudscraper Bypass (Cloudflare)

```python
import cloudscraper

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
response = scraper.get('https://api.example.com/endpoint')
```

### Complete API Replicator

```python
import cloudscraper, random, string

class APIReplicator:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = cloudscraper.create_scraper()
    
    def generate_token(self):
        chars = string.ascii_letters + string.digits
        token = ''.join(random.choice(chars) for _ in range(40))
        fixed = "B9dls0fK"
        pos = random.randint(0, len(token))
        return token[:pos] + fixed + token[pos:]
    
    def get(self, endpoint, auth_header=None):
        headers = {'Accept': 'application/json'}
        if auth_header:
            headers[auth_header] = self.generate_token()
        return self.session.get(f"{self.base_url}{endpoint}", headers=headers)
```

---

## Brand Data Extraction

Extract brand info (name, logo, colors, social links, features) from any website:

```python
from scrapling.fetchers import Fetcher
from urllib.parse import urljoin

def extract_brand_data(url: str) -> dict:
    page = Fetcher.get(url)
    
    def text(sel): return (page.css(sel)[0].text if page.css(sel) else None)
    def attr(sel, a): return (page.css(sel)[0].attrib.get(a) if page.css(sel) else None)
    
    brand_name = text('[property="og:site_name"]') or text('h1') or text('title')
    tagline = text('[property="og:description"]') or text('.tagline') or text('header h2')
    logo_url = attr('[rel="icon"]', 'href') or attr('.logo img', 'src')
    if logo_url and not logo_url.startswith('http'): logo_url = urljoin(url, logo_url)
    
    description = text('[property="og:description"]') or attr('[name="description"]', 'content')
    
    social_links = {}
    for p in ['twitter', 'github', 'linkedin', 'youtube']:
        link = attr(f'a[href*="{p}"]', 'href')
        if link: social_links[p] = link
    
    features = [card.text.strip() for card in page.css('[class*="feature"], .feature-card')[:6] if card.text]
    
    return {
        'brandName': brand_name, 'tagline': tagline, 'description': description,
        'features': features, 'logoUrl': logo_url, 'socialLinks': social_links,
        'screenshotUrl': f"https://image.thum.io/get/width/1200/crop/800/{url}"
    }
```

---

## Sitemap Crawl

```python
from scrapling.fetchers import Fetcher
import re

def get_sitemap_urls(base_url: str, max_urls: int = 100) -> list:
    """Extract URLs from sitemap.xml / robots.txt."""
    sitemap_urls = [f"{base_url}/sitemap.xml", f"{base_url}/sitemap-index.xml"]
    # Check robots.txt first
    try:
        robots = Fetcher.get(f"{base_url}/robots.txt")
        if robots.status == 200:
            sitemap_urls = re.findall(r'Sitemap:\s*(\S+)', robots.text, re.IGNORECASE) + sitemap_urls
    except: pass
    
    all_urls = []
    for sm in sitemap_urls:
        try:
            page = Fetcher.get(sm, timeout=10)
            if page.status == 200 and '<?xml' in page.text:
                urls = re.findall(r'<loc>([^<]+)</loc>', page.text)
                all_urls.extend(urls[:max_urls])
        except: continue
    return list(set(all_urls))[:max_urls]
```
