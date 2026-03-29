#!/bin/bash
# 立即可用的舆倩监测脚本（只使用公开 API）
# 无需 Browser Bridge 扩展

KEYWORDS_FILE="/Users/rayxu/.openclaw/workspace/scripts/keywords.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "==================================="
echo "📊 舆倩监测报告 - $TIMESTAMP"
echo "==================================="

# 读取关键词
KEYWORDS=""
if [ -f "$KEYWORDS_FILE" ]; then
    KEYWORDS=$(cat "$KEYWORDS_FILE" | tr '\n' ' ')
fi

if [ -z "$KEYWORDS" ]; then
    echo "⚠️ 未提供关键词，只获取各平台热门内容"
else
    echo "关键词: $KEYWORDS"
fi

echo ""

# Hacker News
echo "📰 Hacker News 热门"
echo "---"
opencli hackernews top --limit 10

echo ""

# B站热榜
echo "📺 B站 热门"
echo "---"
opencli bilibili hot --limit 10

echo ""

# 微博热搜
echo "🐦 微博热搜"
echo "---"
opencli weibo hot --limit 10

echo ""

# V2EX热门
echo "🐧 V2EX 热门"
echo "---"
opencli v2ex hot --limit 10

echo ""

# DEV.to热门
echo "💻 DEV.to 热门"
echo "---"
opencli devto top --limit 10

echo ""

# StackOverflow热门
echo "💻 StackOverflow 热门"
echo "---"
opencli stackoverflow hot --limit 10

echo ""

# Wikipedia搜索
if [ -n "$KEYWORDS" ]; then
    echo "📚 Wikipedia 搜索"
    echo "---"
    for keyword in $KEYWORDS; do
        echo "搜索: $keyword"
        opencli wikipedia search "$keyword" --limit 5
        echo ""
    done
fi

echo "==================================="
echo "✅ 监测完成"
echo "==================================="
