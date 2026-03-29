#!/bin/bash
# 舆情监测 + 自动报告脚本
# 每天执行一次，并发送简报到Telegram

# 配置
SCRIPT_DIR="/Users/rayxu/.openclaw/workspace/scripts"
REPORT_DIR="$SCRIPT_DIR/reports"
KEYWORDS_FILE="$SCRIPT_DIR/keywords.txt"
LOG_FILE="$SCRIPT_DIR/sentiment-monitor-cron.log"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 记录开始时间
echo "========================================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - 开始舆情监测" >> "$LOG_FILE"

# 读取关键词（排除注释和空行）
KEYWORDS=$(grep -v '^#' "$KEYWORDS_FILE" | grep -v '^$' | tr '\n' ' ')

echo "关键词: $KEYWORDS" >> "$LOG_FILE"

# 运行Python脚本
if [ -n "$KEYWORDS" ]; then
    python3 simple-sentiment.py --keywords $KEYWORDS 2>&1 >> "$LOG_FILE"
else
    python3 simple-sentiment.py 2>&1 >> "$LOG_FILE"
fi

# 获取最新报告
LATEST_REPORT=$(ls -t "$REPORT_DIR"/simple-sentiment-*.json 2>/dev/null | head -1)

if [ -z "$LATEST_REPORT" ]; then
    echo "❌ 未找到报告文件" >> "$LOG_FILE"
    exit 1
fi

echo "报告文件: $LATEST_REPORT" >> "$LOG_FILE"

# 调用Python生成简报并发送
python3 - <<'PYTHON_SCRIPT'
import json
import os
from datetime import datetime

# 报告目录
report_dir = "/Users/rayxu/.openclaw/workspace/scripts/reports"
latest_report = os.popen("ls -t " + report_dir + "/simple-sentiment-*.json 2>/dev/null | head -1").read().strip()

if not latest_report or not os.path.exists(latest_report):
    print("❌ 未找到报告文件")
    exit(1)

# 读取报告
with open(latest_report, 'r', encoding='utf-8') as f:
    data = json.load(f)

timestamp = data.get('timestamp', '')
keywords = data.get('keywords', [])
results = data.get('results', {})

# 生成简报
report_lines = []
report_lines.append("📊 舆情监测简报")
report_lines.append(f"📅 {timestamp}")
report_lines.append(f"🔑 关键词: {', '.join(keywords)}")
report_lines.append("")

# Hacker News Top 5
if 'hackernews' in results and results['hackernews']:
    report_lines.append("📰 Hacker News Top 5")
    for item in results['hackernews'][:5]:
        score = item.get('score', 0)
        title = item.get('title', '')[:50] + ('...' if len(item.get('title', '')) > 50 else '')
        report_lines.append(f"  {item.get('rank', '')}. {title} ({score}⭐)")

# V2EX Top 5
if 'v2ex' in results and results['v2ex']:
    report_lines.append("")
    report_lines.append("🐧 V2EX Top 5")
    for item in results['v2ex'][:5]:
        replies = item.get('replies', 0)
        title = item.get('title', '')[:50] + ('...' if len(item.get('title', '')) > 50 else '')
        report_lines.append(f"  {item.get('rank', '')}. {title} ({replies}💬)")

# 微博热搜 Top 5
if 'weibo' in results and results['weibo'].get('hot'):
    report_lines.append("")
    report_lines.append("🐦 微博热搜 Top 5")
    for item in results['weibo']['hot'][:5]:
        num = item.get('num', 0)
        title = item.get('title', '')[:50] + ('...' if len(item.get('title', '')) > 50 else '')
        report_lines.append(f"  {item.get('rank', '')}. {title} 🔥{num}")

# B站热门 Top 5
if 'bilibili' in results and results['bilibili'].get('hot'):
    report_lines.append("")
    report_lines.append("📺 B站热门 Top 5")
    for item in results['bilibili']['hot'][:5]:
        view = item.get('view', 0)
        title = item.get('title', '')[:50] + ('...' if len(item.get('title', '')) > 50 else '')
        report_lines.append(f"  {item.get('rank', '')}. {title} 👁️{view}")

# 关键词搜索结果摘要
report_lines.append("")
report_lines.append("🔍 关键词搜索摘要")

for keyword in keywords:
    keyword_results = []
    # 搜索Hacker News
    if 'hackernews' in results and results['hackernews']:
        hn_hits = sum(1 for item in results['hackernews'] if keyword.lower() in item.get('title', '').lower())
        if hn_hits > 0:
            keyword_results.append(f"HackerNews: {hn_hits}")

    # 搜索Wikipedia
    if 'wikipedia' in results and results['wikipedia']:
        wiki_data = next((w for w in results['wikipedia'] if w.get('keyword') == keyword), None)
        if wiki_data and wiki_data.get('results'):
            keyword_results.append(f"Wikipedia: {len(wiki_data['results'])}")

    if keyword_results:
        report_lines.append(f"  • {keyword}: {', '.join(keyword_results)}")
    else:
        report_lines.append(f"  • {keyword}: 未发现相关内容")

report_lines.append("")
report_lines.append("📄 详细报告见: scripts/reports/")

# 保存简报
brief_text = '\n'.join(report_lines)
brief_file = "/tmp/sentiment-brief.txt"
with open(brief_file, 'w', encoding='utf-8') as f:
    f.write(brief_text)

print(brief_text)
PYTHON_SCRIPT

# 捕获Python输出并保存到临时文件
BRIEF_FILE="/tmp/sentiment-brief.txt"

# 发送到Telegram（通过OpenClaw的message工具）
# 注意：这个会通过OpenClaw的配置自动路由到当前用户

# 保存结果
echo "$(date '+%Y-%m-%d %H:%M:%S') - 舆情监测完成" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 输出简报（用于发送）
cat "$BRIEF_FILE"
