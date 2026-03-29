#!/usr/bin/env python3
"""
多平台舆情监测工具
支持: B站、抖音、小红书、微博
"""

import subprocess
import json
import argparse
from datetime import datetime
from pathlib import Path

class SentimentMonitor:
    def __init__(self, keywords=None):
        self.keywords = keywords or []
        self.results = {
            'bilibili': {'hot': [], 'search': []},
            'tiktok': {'explore': [], 'search': []},
            'xiaohongshu': {'search': [], 'feed': []},
            'weibo': {'hot': [], 'search': []}
        }

    def run_opencli(self, command):
        """执行 opencli 命令并返回结果"""
        try:
            result = subprocess.run(
                ['opencli'] + command,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # 尝试解析 JSON 输出
                try:
                    return json.loads(result.stdout)
                except:
                    return result.stdout
            else:
                print(f"❌ 命令失败: {' '.join(command)}")
                print(f"错误: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print(f"⏱️ 命令超时: {' '.join(command)}")
            return None
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            return None

    def monitor_bilibili(self):
        """监测 B站"""
        print("\n📺 监测 B站...")
        print("-" * 40)

        # 热榜
        hot = self.run_opencli(['bilibili', 'hot', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['bilibili']['hot'] = hot
            print(f"✅ B站热榜: {len(hot) if isinstance(hot, list) else 'N/A'} 条")

        # 搜索
        if self.keywords:
            for keyword in self.keywords:
                search = self.run_opencli(['bilibili', 'search', keyword, '--limit', '10', '--format', 'json'])
                if search:
                    self.results['bilibili']['search'].append({
                        'keyword': keyword,
                        'results': search
                    })
                    count = len(search) if isinstance(search, list) else 'N/A'
                    print(f"✅ B站搜索 [{keyword}]: {count} 条")

    def monitor_tiktok(self):
        """监测 TikTok/抖音"""
        print("\n📱 监测 抖音...")
        print("-" * 40)

        # 探索页
        explore = self.run_opencli(['tiktok', 'explore', '--format', 'json'])
        if explore:
            self.results['tiktok']['explore'] = explore
            count = len(explore) if isinstance(explore, list) else 'N/A'
            print(f"✅ 抖音探索: {count} 条")

        # 搜索
        if self.keywords:
            for keyword in self.keywords:
                search = self.run_opencli(['tiktok', 'search', keyword, '--format', 'json'])
                if search:
                    self.results['tiktok']['search'].append({
                        'keyword': keyword,
                        'results': search
                    })
                    count = len(search) if isinstance(search, list) else 'N/A'
                    print(f"✅ 抖音搜索 [{keyword}]: {count} 条")

    def monitor_xiaohongshu(self):
        """监测小红书"""
        print("\n📕 监测 小红书...")
        print("-" * 40)

        # 推荐 Feed
        feed = self.run_opencli(['xiaohongshu', 'feed', '--limit', '10', '--format', 'json'])
        if feed:
            self.results['xiaohongshu']['feed'] = feed
            count = len(feed) if isinstance(feed, list) else 'N/A'
            print(f"✅ 小红书推荐: {count} 条")

        # 搜索
        if self.keywords:
            for keyword in self.keywords:
                search = self.run_opencli(['xiaohongshu', 'search', keyword, '--limit', '10', '--format', 'json'])
                if search:
                    self.results['xiaohongshu']['search'].append({
                        'keyword': keyword,
                        'results': search
                    })
                    count = len(search) if isinstance(search, list) else 'N/A'
                    print(f"✅ 小红书搜索 [{keyword}]: {count} 条")

    def monitor_weibo(self):
        """监测微博"""
        print("\n🐦 监测 微博...")
        print("-" * 40)

        # 热搜
        hot = self.run_opencli(['weibo', 'hot', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['weibo']['hot'] = hot
            count = len(hot) if isinstance(hot, list) else 'N/A'
            print(f"✅ 微博热搜: {count} 条")

        # 搜索
        if self.keywords:
            for keyword in self.keywords:
                search = self.run_opencli(['weibo', 'search', keyword, '--limit', '10', '--format', 'json'])
                if search:
                    self.results['weibo']['search'].append({
                        'keyword': keyword,
                        'results': search
                    })
                    count = len(search) if isinstance(search, list) else 'N/A'
                    print(f"✅ 微博搜索 [{keyword}]: {count} 条")

    def run(self, platforms=None):
        """运行监测"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print("=" * 50)
        print(f"📊 舆情监测报告")
        print(f"时间: {timestamp}")
        print(f"关键词: {', '.join(self.keywords) if self.keywords else '无'}")
        print("=" * 50)

        if not platforms or 'bilibili' in platforms:
            self.monitor_bilibili()
        if not platforms or 'tiktok' in platforms:
            self.monitor_tiktok()
        if not platforms or 'xiaohongshu' in platforms:
            self.monitor_xiaohongshu()
        if not platforms or 'weibo' in platforms:
            self.monitor_weibo()

        self.save_report(timestamp)

    def save_report(self, timestamp):
        """保存报告到文件"""
        report_dir = Path(__file__).parent / 'reports'
        report_dir.mkdir(exist_ok=True)

        filename = f"sentiment-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        filepath = report_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'keywords': self.keywords,
                'results': self.results
            }, f, ensure_ascii=False, indent=2)

        print(f"\n💾 报告已保存: {filepath}")

    def print_summary(self):
        """打印汇总统计"""
        print("\n" + "=" * 50)
        print("📈 监测汇总")
        print("=" * 50)

        # B站
        hot_count = len(self.results['bilibili']['hot']) if isinstance(self.results['bilibili']['hot'], list) else 0
        search_count = sum(len(r['results']) if isinstance(r['results'], list) else 0
                        for r in self.results['bilibili']['search'])
        print(f"📺 B站: 热榜 {hot_count} 条 | 搜索 {search_count} 条")

        # 抖音
        explore_count = len(self.results['tiktok']['explore']) if isinstance(self.results['tiktok']['explore'], list) else 0
        search_count = sum(len(r['results']) if isinstance(r['results'], list) else 0
                        for r in self.results['tiktok']['search'])
        print(f"📱 抖音: 探索 {explore_count} 条 | 搜索 {search_count} 条")

        # 小红书
        feed_count = len(self.results['xiaohongshu']['feed']) if isinstance(self.results['xiaohongshu']['feed'], list) else 0
        search_count = sum(len(r['results']) if isinstance(r['results'], list) else 0
                        for r in self.results['xiaohongshu']['search'])
        print(f"📕 小红书: 推荐 {feed_count} 条 | 搜索 {search_count} 条")

        # 微博
        hot_count = len(self.results['weibo']['hot']) if isinstance(self.results['weibo']['hot'], list) else 0
        search_count = sum(len(r['results']) if isinstance(r['results'], list) else 0
                        for r in self.results['weibo']['search'])
        print(f"🐦 微博: 热搜 {hot_count} 条 | 搜索 {search_count} 条")

        print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description='多平台舆情监测工具')
    parser.add_argument('-k', '--keywords', nargs='+', help='搜索关键词列表')
    parser.add_argument('-p', '--platforms', nargs='+',
                    choices=['bilibili', 'tiktok', 'xiaohongshu', 'weibo'],
                    help='监测平台列表（默认：全部）')
    parser.add_argument('--summary', action='store_true', help='只显示汇总统计')

    args = parser.parse_args()

    # 读取关键词配置文件
    keywords = args.keywords
    if not keywords:
        keywords_file = Path(__file__).parent / 'keywords.txt'
        if keywords_file.exists():
            with open(keywords_file, encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip()]

    if not keywords:
        print("⚠️ 未提供关键词，将只获取各平台热门内容")
        keywords = []

    # 创建监测器并运行
    monitor = SentimentMonitor(keywords=keywords)
    monitor.run(platforms=args.platforms)

    if args.summary:
        monitor.print_summary()

if __name__ == '__main__':
    main()
