#!/bin/bash
# 舆情监测脚本 - B站、抖音、小红书、微博

KEYWORDS="$1"  # 搜索关键词
LIMIT=10        # 结果数量

echo "==================================="
echo "📊 舆情监测报告 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "关键词: $KEYWORDS"
echo "==================================="

echo ""
echo "📺 B站 (Bilibili)"
echo "---"
opencli bilibili hot --limit 5 || echo "❌ B站热榜获取失败"
echo ""
echo "🔍 B站搜索: $KEYWORDS"
opencli bilibili search "$KEYWORDS" --limit $LIMIT || echo "❌ B站搜索失败"

echo ""
echo "📱 抖音 (TikTok)"
echo "---"
echo "🔍 抖音搜索: $KEYWORDS"
opencli tiktok search "$KEYWORDS" || echo "❌ 抖音搜索失败"

echo ""
echo "📕 小红书"
echo "---"
echo "🔍 小红书搜索: $KEYWORDS"
opencli xiaohongshu search "$KEYWORDS" --limit $LIMIT || echo "❌ 小红书搜索失败"

echo ""
echo "🐦 微博"
echo "---"
opencli weibo hot --limit 5 || echo "❌ 微博热搜获取失败"
echo ""
echo "🔍 微博搜索: $KEYWORDS"
opencli weibo search "$KEYWORDS" --limit $LIMIT || echo "❌ 微博搜索失败"

echo ""
echo "==================================="
echo "✅ 监测完成"
echo "==================================="
