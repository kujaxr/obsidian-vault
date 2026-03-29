#!/usr/bin/env python3
"""
文献监控脚本 - 多源检索
- Semantic Scholar API (免费无需Key)
- OpenAlex API (免费无需Key)
- Crossref API (免费无需Key)
- Google Scholar (scholarly库，非官方)
- ResearchGate (网页抓取，非官方)
"""

import requests
import json
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import sys

# 尝试导入scholarly（Google Scholar非官方API）
try:
    import scholarly
    HAS_SCHOLARLY = True
except ImportError:
    HAS_SCHOLARLY = False
    print("⚠️ scholarly库未安装，Google Scholar检索将跳过")
    print("   安装命令: pip install scholarly")

# 尝试导入BeautifulSoup（用于ResearchGate抓取）
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("⚠️ beautifulsoup4库未安装，ResearchGate检索将跳过")
    print("   安装命令: pip install beautifulsoup4")

# 配置
SCRIPT_DIR = Path("/Users/rayxu/.openclaw/workspace/scripts")
REPORT_DIR = SCRIPT_DIR / "reports"
LITERATURE_DIR = SCRIPT_DIR / "literature"
LOG_FILE = SCRIPT_DIR / "literature-monitor.log"

# 确保目录存在
REPORT_DIR.mkdir(exist_ok=True)
LITERATURE_DIR.mkdir(exist_ok=True)


def log(message: str):
    """日志记录"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {message}\n")
    print(f"{timestamp} - {message}")


def format_number(num: int) -> str:
    """格式化数字"""
    if num >= 10000:
        return f"{num/10000:.1f}万"
    return str(num)


def search_semantic_scholar(query: str, limit: int = 10, days: int = 30) -> List[Dict]:
    """搜索Semantic Scholar API"""
    log(f"🔍 Semantic Scholar: {query}")

    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,citationCount,externalIds,url,openAccessPdf,venue"
    }

    # 添加时间过滤（如果API支持）
    # 注意：Semantic Scholar API不直接支持日期过滤，这里不做限制

    results = []
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            results = data.get("data", [])
            log(f"   ✅ 找到 {len(results)} 条结果")
        else:
            log(f"   ❌ HTTP {response.status_code}")
    except Exception as e:
        log(f"   ❌ 错误: {e}")

    return results


def search_openalex(query: str, limit: int = 10) -> List[Dict]:
    """搜索OpenAlex API"""
    log(f"🔍 OpenAlex: {query}")

    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per-page": limit,
        "select": "title,authorships,publication_year,abstract_inverted_index, cited_by_count, primary_location,doi,id"
    }

    results = []
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        results = data.get("results", [])
        log(f"   ✅ 找到 {len(results)} 条结果")
    except Exception as e:
        log(f"   ❌ 错误: {e}")
        results = []

    return results


def search_crossref(query: str, limit: int = 10) -> List[Dict]:
    """搜索Crossref API"""
    log(f"🔍 Crossref: {query}")

    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": limit,
        "select": "DOI,title,author,published-print,is-referenced-by-count,URL"
    }

    results = []
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        results = data.get("message", {}).get("items", [])
        log(f"   ✅ 找到 {len(results)} 条结果")
    except Exception as e:
        log(f"   ❌ 错误: {e}")
        results = []

    return results


def search_google_scholar(query: str, limit: int = 10) -> List[Dict]:
    """搜索Google Scholar（使用scholarly库）"""
    if not HAS_SCHOLARLY:
        log(f"🔍 Google Scholar: scholarly未安装，跳过")
        return []

    log(f"🔍 Google Scholar: {query}")

    results = []
    try:
        # 搜索
        search_results = scholarly.search_papers(query)

        for i, paper in enumerate(search_results):
            if i >= limit:
                break

            result = {
                "title": paper.get("bib", {}).get("title", ""),
                "authors": paper.get("bib", {}).get("author", []),
                "year": paper.get("bib", {}).get("pub_year", ""),
                "citation_count": paper.get("num_citations", 0),
                "abstract": paper.get("bib", {}).get("abstract", "")[:500],
                "url": paper.get("pub_url", ""),
                "source": "Google Scholar"
            }
            results.append(result)

            # 避免请求过快
            time.sleep(1)

        log(f"   ✅ 找到 {len(results)} 条结果")

    except Exception as e:
        log(f"   ❌ 错误: {e}")

    return results


def search_researchgate(query: str, limit: int = 10) -> List[Dict]:
    """搜索ResearchGate（网页抓取）"""
    if not HAS_BS4:
        log(f"🔍 ResearchGate: beautifulsoup4未安装，跳过")
        return []

    log(f"🔍 ResearchGate: {query}")

    # ResearchGate没有官方API，这里用搜索结果页面
    # 注意：这种方式可能不稳定
    url = f"https://www.researchgate.net/search/researcher?q={requests.utils.quote(query)}"

    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # ResearchGate页面结构可能变化，这里只是示例
            # 实际可能需要更复杂的解析
            papers = soup.select(".nova-legacy-v-publication-item__title")

            for i, paper in enumerate(papers[:limit]):
                title_elem = paper.select_one("a")
                if title_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": title_elem.get("href", ""),
                        "source": "ResearchGate"
                    })

            log(f"   ✅ 找到 {len(results)} 条结果")
        else:
            log(f"   ❌ HTTP {response.status_code}")

    except Exception as e:
        log(f"   ❌ 错误: {e}")

    return results


def search_arxiv(query: str, limit: int = 10) -> List[Dict]:
    """搜索arXiv预印本"""
    log(f"🔍 arXiv: {query}")

    # arXiv API
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    results = []
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            # 解析XML响应
            soup = BeautifulSoup(response.text, "xml")
            entries = soup.find_all("entry")

            for entry in entries:
                authors = [author.get_text() for author in entry.find_all("name")]

                result = {
                    "title": entry.title.get_text() if entry.title else "",
                    "authors": authors[:5],  # 只取前5个作者
                    "year": entry.published.get_text()[:4] if entry.published else "",
                    "abstract": entry.summary.get_text()[:500] if entry.summary else "",
                    "url": entry.id.get_text() if entry.id else "",
                    "citation_count": 0,
                    "source": "arXiv"
                }
                results.append(result)

            log(f"   ✅ 找到 {len(results)} 条结果")

    except Exception as e:
        log(f"   ❌ 错误: {e}")

    return results


def parse_authors(authors_data: List) -> str:
    """解析作者列表"""
    if not authors_data:
        return "未知"

    if isinstance(authors_data[0], str):
        # Crossref格式
        authors = authors_data[:3]
    elif isinstance(authors_data[0], dict):
        # Semantic Scholar格式
        authors = [a.get("name", "") for a in authors_data[:3]]
    else:
        authors = authors_data[:3]

    return ", ".join([a for a in authors if a]) + ("..." if len(authors_data) > 3 else "")


def run_literature_search(keywords: List[str], platforms: List[str] = None) -> Dict:
    """运行文献搜索"""
    log("=" * 60)
    log("文献监控开始")

    if platforms is None:
        platforms = ["semantic_scholar", "openalex", "crossref", "arxiv"]

    all_results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "keywords": keywords,
        "sources": platforms,
        "papers": []
    }

    seen_titles = set()  # 去重

    for keyword in keywords:
        log(f"\n📌 搜索关键词: {keyword}")
        print("-" * 40)

        # Semantic Scholar
        if "semantic_scholar" in platforms:
            for paper in search_semantic_scholar(keyword, limit=5):
                title = paper.get("title", "")[:100]
                if title not in seen_titles:
                    seen_titles.add(title)
                    all_results["papers"].append({
                        "title": paper.get("title", ""),
                        "authors": parse_authors(paper.get("authors", [])),
                        "year": paper.get("year", ""),
                        "citation_count": paper.get("citationCount", 0),
                        "abstract": (paper.get("abstract", "") or "")[:300],
                        "url": paper.get("url", ""),
                        "pdf_url": paper.get("openAccessPdf", {}).get("url") if isinstance(paper.get("openAccessPdf"), dict) else None,
                        "source": "Semantic Scholar"
                    })
            time.sleep(1)  # 避免请求过快

        # OpenAlex
        if "openalex" in platforms:
            for paper in search_openalex(keyword, limit=5):
                title = paper.get("title", "")[:100]
                if title not in seen_titles:
                    seen_titles.add(title)

                    # 解析摘要
                    abstract = ""
                    if paper.get("abstract_inverted_index"):
                        # 重建摘要
                        abstract_words = []
                        idx = paper["abstract_inverted_index"]
                        for word, positions in idx.items():
                            for pos in positions:
                                abstract_words.append((pos, word))
                        abstract_words.sort(key=lambda x: x[0])
                        abstract = " ".join([w[1] for w in abstract_words])[:300]

                    authors = []
                    for auth in paper.get("authorships", [])[:3]:
                        author_name = auth.get("author", {}).get("display_name", "")
                        if author_name:
                            authors.append(author_name)

                    all_results["papers"].append({
                        "title": paper.get("title", ""),
                        "authors": ", ".join(authors) + ("..." if len(paper.get("authorships", [])) > 3 else ""),
                        "year": paper.get("publication_year", ""),
                        "citation_count": paper.get("cited_by_count", 0),
                        "abstract": abstract,
                        "url": paper.get("doi", ""),
                        "pdf_url": None,
                        "source": "OpenAlex"
                    })
            time.sleep(1)

        # Crossref
        if "crossref" in platforms:
            for paper in search_crossref(keyword, limit=5):
                title_elem = paper.get("title", [""])[0][:100] if paper.get("title") else ""
                if title_elem and title_elem not in seen_titles:
                    seen_titles.add(title_elem)

                    authors_raw = paper.get("author", [])
                    authors_list = []
                    for a in authors_raw:
                        name = a.get("family", "") or a.get("given", "")
                        if name:
                            authors_list.append(name)

                    year = ""
                    if paper.get("published-print"):
                        dates = paper["published-print"].get("date-parts", [[]])
                        if dates and dates[0]:
                            year = str(dates[0][0])

                    all_results["papers"].append({
                        "title": paper.get("title", [""])[0] if paper.get("title") else "",
                        "authors": ", ".join(authors_list[:3]) + ("..." if len(authors_list) > 3 else ""),
                        "year": year,
                        "citation_count": paper.get("is-referenced-by-count", 0),
                        "abstract": "",
                        "url": paper.get("URL", ""),
                        "pdf_url": None,
                        "source": "Crossref"
                    })
            time.sleep(1)

        # arXiv
        if "arxiv" in platforms:
            for paper in search_arxiv(keyword, limit=3):
                title = paper.get("title", "")[:100]
                if title not in seen_titles:
                    seen_titles.add(title)
                    all_results["papers"].append({
                        "title": paper.get("title", ""),
                        "authors": ", ".join(paper.get("authors", [])[:3]),
                        "year": paper.get("year", ""),
                        "citation_count": 0,
                        "abstract": paper.get("abstract", ""),
                        "url": paper.get("url", ""),
                        "pdf_url": paper.get("url", "").replace("/abs/", "/pdf/") + ".pdf",
                        "source": "arXiv"
                    })
            time.sleep(1)

        # Google Scholar (较慢，每个关键词约30秒)
        if "google_scholar" in platforms and HAS_SCHOLARLY:
            for paper in search_google_scholar(keyword, limit=3):
                title = paper.get("title", "")[:100]
                if title not in seen_titles:
                    seen_titles.add(title)
                    all_results["papers"].append({
                        "title": paper.get("title", ""),
                        "authors": ", ".join(paper.get("authors", [])[:3]),
                        "year": paper.get("year", ""),
                        "citation_count": paper.get("citation_count", 0),
                        "abstract": paper.get("abstract", ""),
                        "url": paper.get("url", ""),
                        "pdf_url": None,
                        "source": "Google Scholar"
                    })
            time.sleep(3)

        # ResearchGate (不太稳定)
        if "researchgate" in platforms and HAS_BS4:
            for paper in search_researchgate(keyword, limit=3):
                title = paper.get("title", "")[:100]
                if title not in seen_titles:
                    seen_titles.add(title)
                    all_results["papers"].append({
                        "title": paper.get("title", ""),
                        "authors": "",
                        "year": "",
                        "citation_count": 0,
                        "abstract": "",
                        "url": paper.get("url", ""),
                        "pdf_url": None,
                        "source": "ResearchGate"
                    })
            time.sleep(2)

    log(f"\n✅ 共找到 {len(all_results['papers'])} 篇文献")

    # 保存报告
    report_file = LITERATURE_DIR / f"literature-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    log(f"💾 报告已保存: {report_file}")

    log("=" * 60)

    return all_results


def generate_brief(results: Dict) -> str:
    """生成简报"""
    lines = []
    lines.append("📚 文献监控简报")
    lines.append(f"📅 {results['timestamp']}")
    lines.append(f"🔑 关键词: {', '.join(results['keywords'])}")
    lines.append(f"📊 数据来源: {', '.join(results['sources'])}")
    lines.append(f"📄 共 {len(results['papers'])} 篇文献")
    lines.append("")
    lines.append("━" * 40)

    # 按来源分组
    by_source = {}
    for paper in results["papers"]:
        source = paper.get("source", "Unknown")
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(paper)

    # 输出每个来源的前5篇
    for source, papers in by_source.items():
        lines.append(f"\n🔗 {source} ({len(papers)}篇)")
        lines.append("-" * 40)

        for i, paper in enumerate(papers[:5], 1):
            title = paper.get("title", "无标题")
            if len(title) > 60:
                title = title[:60] + "..."

            authors = paper.get("authors", "")
            if len(authors) > 40:
                authors = authors[:40] + "..."

            year = paper.get("year", "?")
            citations = paper.get("citation_count", 0)

            lines.append(f"  {i}. {title}")
            if authors:
                lines.append(f"     👥 {authors}")
            lines.append(f"     📅 {year} | ⭐ {citations}次引用")

            url = paper.get("url", "")
            if url:
                # 截断URL显示
                if len(url) > 50:
                    url = url[:50] + "..."
                lines.append(f"     🔗 {url}")

            if paper.get("pdf_url"):
                lines.append(f"     📄 PDF可下载")

            lines.append("")

    lines.append("━" * 40)
    lines.append("📁 完整报告: scripts/literature/")

    return "\n".join(lines)


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 从命令行参数获取关键词
        keywords = sys.argv[1:]
    else:
        # 从文件读取关键词
        keywords_file = SCRIPT_DIR / "literature_keywords.txt"
        if keywords_file.exists():
            with open(keywords_file, encoding="utf-8") as f:
                keywords = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        else:
            # 默认关键词
            keywords = [
                "functional coating automotive",
                "new material painting process",
                "nano coating surface treatment",
                "automotive paint adhesion"
            ]
            log("⚠️ 未找到关键词文件，使用默认关键词")

    if not keywords:
        log("❌ 没有关键词，退出")
        return 1

    # 运行搜索
    results = run_literature_search(keywords)

    # 生成简报
    brief = generate_brief(results)
    print("\n" + brief)

    # 保存简报
    brief_file = LITERATURE_DIR / f"literature-brief-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(brief_file, "w", encoding="utf-8") as f:
        f.write(brief)
    log(f"💾 简报已保存: {brief_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
