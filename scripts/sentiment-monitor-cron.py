#!/usr/bin/env python3
"""
舆情监测定时任务脚本
- 运行simple-sentiment.py生成报告
- 解析报告生成简报
- 通过Telegram Bot发送到Telegram
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置
SCRIPT_DIR = Path("/Users/rayxu/.openclaw/workspace/scripts")
REPORT_DIR = SCRIPT_DIR / "reports"
KEYWORDS_FILE = SCRIPT_DIR / "keywords.txt"
LOG_FILE = SCRIPT_DIR / "sentiment-monitor-cron.log"
BRIEF_FILE = Path("/tmp/sentiment-brief.txt")
BOT_TOKEN = "8132195706:AAHDfR05pmH7Z_-Dv_3MmFC6PCkJXHhR4mI"
TELEGRAM_TARGET = "905207854"


def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {message}\n")
    print(f"{timestamp} - {message}")


def send_telegram(text: str):
    """通过Telegram Bot发送消息"""
    import urllib.request
    import urllib.parse

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_TARGET,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        req = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(data).encode("utf-8"),
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                log("✅ Telegram消息发送成功")
            else:
                log(f"❌ Telegram发送失败: {result}")
    except Exception as e:
        log(f"❌ Telegram发送出错: {e}")


def read_keywords():
    """读取关键词"""
    if not KEYWORDS_FILE.exists():
        return []

    keywords = []
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                keywords.append(line)

    return keywords


def run_monitor(keywords):
    """运行监测脚本"""
    log("开始运行舆情监测...")

    cmd = [sys.executable, str(SCRIPT_DIR / "simple-sentiment.py")]
    if keywords:
        cmd.extend(["--keywords"] + keywords)

    try:
        result = subprocess.run(
            cmd,
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        if result.returncode != 0:
            log(f"监测脚本执行失败: {result.stderr}")
            return False

        log("监测脚本执行成功")
        return True

    except subprocess.TimeoutExpired:
        log("监测脚本执行超时")
        return False
    except Exception as e:
        log(f"监测脚本执行出错: {e}")
        return False


def get_latest_report():
    """获取最新报告"""
    reports = sorted(REPORT_DIR.glob("simple-sentiment-*.json"), reverse=True)

    if not reports:
        log("未找到任何报告")
        return None

    latest = reports[0]
    log(f"最新报告: {latest.name}")
    return latest


def generate_brief(report_path):
    """生成简报"""
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamp = data.get("timestamp", "")
    keywords = data.get("keywords", [])
    results = data.get("results", {})

    lines = []
    lines.append("📊 舆情监测简报")
    lines.append(f"📅 {timestamp}")
    if keywords:
        lines.append(f"🔑 关键词: {', '.join(keywords)}")
    lines.append("")

    # Hacker News Top 5
    if "hackernews" in results and results["hackernews"]:
        lines.append("📰 Hacker News Top 5")
        for item in results["hackernews"][:5]:
            score = item.get("score", 0)
            title = item.get("title", "")
            if len(title) > 45:
                title = title[:45] + "..."
            lines.append(f"  {item.get('rank', '')}. {title} ({score}⭐)")

    # V2EX Top 5
    if "v2ex" in results and results["v2ex"]:
        lines.append("")
        lines.append("🐧 V2EX Top 5")
        for item in results["v2ex"][:5]:
            replies = item.get("replies", 0)
            title = item.get("title", "")
            if len(title) > 45:
                title = title[:45] + "..."
            lines.append(f"  {item.get('rank', '')}. {title} ({replies}💬)")

    # 微博热搜 Top 5
    if "weibo" in results and results["weibo"].get("hot"):
        lines.append("")
        lines.append("🐦 微博热搜 Top 5")
        for item in results["weibo"]["hot"][:5]:
            hot_value = item.get("hot_value", 0)
            # 格式化数字：553224 -> 55.3万
            if hot_value >= 10000:
                display_value = f"{hot_value/10000:.1f}万"
            else:
                display_value = str(hot_value)
            title = item.get("word", item.get("title", ""))
            label = item.get("label", "")
            if len(title) > 40:
                title = title[:40] + "..."
            lines.append(f"  {item.get('rank', '')}. {title} 🔥{display_value}{label}")

    # B站热门 Top 5
    if "bilibili" in results and results["bilibili"].get("hot"):
        lines.append("")
        lines.append("📺 B站热门 Top 5")
        for item in results["bilibili"]["hot"][:5]:
            play = item.get("play", 0)
            # 格式化播放量
            if play >= 10000:
                display_play = f"{play/10000:.1f}万"
            else:
                display_play = str(play)
            title = item.get("title", "")
            if len(title) > 40:
                title = title[:40] + "..."
            lines.append(f"  {item.get('rank', '')}. {title} ▶️{display_play}")

    # 小红书搜索 Top 3
    if "xiaohongshu" in results and results["xiaohongshu"].get("search"):
        lines.append("")
        lines.append("📕 小红书搜索")
        for search_group in results["xiaohongshu"]["search"][:3]:  # 只显示前3个关键词
            keyword = search_group.get("keyword", "")
            search_results = search_group.get("results", [])
            lines.append(f"  🔍 {keyword}:")
            for item in search_results[:3]:  # 每个关键词显示3条
                likes = item.get("likes", "0")
                title = item.get("title", "")
                if len(title) > 40:
                    title = title[:40] + "..."
                lines.append(f"    • {title} ❤️{likes}")

    # 关键词搜索摘要
    lines.append("")
    lines.append("🔍 关键词命中统计")

    for keyword in keywords:
        hits = []

        # 搜索Hacker News
        if "hackernews" in results and results["hackernews"]:
            hn_hits = sum(
                1 for item in results["hackernews"]
                if keyword.lower() in item.get("title", "").lower()
            )
            if hn_hits > 0:
                hits.append(f"HN:{hn_hits}")

        # 搜索微博热搜
        if "weibo" in results and results["weibo"].get("hot"):
            wb_hits = sum(
                1 for item in results["weibo"]["hot"]
                if keyword in item.get("word", "") or keyword in item.get("title", "")
            )
            if wb_hits > 0:
                hits.append(f"微博:{wb_hits}")

        # 搜索B站热门
        if "bilibili" in results and results["bilibili"].get("hot"):
            bh_hits = sum(
                1 for item in results["bilibili"]["hot"]
                if keyword in item.get("title", "")
            )
            if bh_hits > 0:
                hits.append(f"B站:{bh_hits}")

        # 搜索小红书
        if "xiaohongshu" in results and results["xiaohongshu"].get("search"):
            xhs_data = next(
                (s for s in results["xiaohongshu"]["search"] if s.get("keyword") == keyword),
                None
            )
            if xhs_data and xhs_data.get("results"):
                hits.append(f"小红书:{len(xhs_data['results'])}")

        # Wikipedia
        if "wikipedia" in results and results["wikipedia"]:
            wiki_data = next(
                (w for w in results["wikipedia"] if w.get("keyword") == keyword),
                None
            )
            if wiki_data and wiki_data.get("results"):
                hits.append(f"Wiki:{len(wiki_data['results'])}")

        if hits:
            lines.append(f"  • {keyword}: {', '.join(hits)}")

    lines.append("")
    lines.append("📄 详细报告: scripts/reports/")

    return "\n".join(lines)


def save_brief(brief_text):
    """保存简报到文件"""
    with open(BRIEF_FILE, "w", encoding="utf-8") as f:
        f.write(brief_text)
    log(f"简报已保存: {BRIEF_FILE}")


def main():
    """主函数"""
    log("=" * 60)
    log("舆情监测定时任务开始")

    # 读取关键词
    keywords = read_keywords()
    log(f"关键词: {', '.join(keywords)}")

    # 运行监测
    if not run_monitor(keywords):
        log("❌ 监测失败，退出")
        return 1

    # 获取最新报告
    report_path = get_latest_report()
    if not report_path:
        log("❌ 未找到报告，退出")
        return 1

    # 生成简报
    brief_text = generate_brief(report_path)
    save_brief(brief_text)

    # 通过Telegram Bot发送
    # Telegram消息有4096字符限制
    if len(brief_text) > 4000:
        brief_text = brief_text[:4000] + "\n...(内容过长已截断)"
    send_telegram(brief_text)

    log("=" * 60)
    log("舆情监测定时任务完成")

    return 0


if __name__ == "__main__":
    sys.exit(main())
