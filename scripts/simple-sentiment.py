#!/usr/bin/env python3
"""
简化版舆情监测 - 只使用公开 API 平台
不需要 Browser Bridge 扩展
"""

import subprocess
import json
import argparse
from datetime import datetime
from pathlib import Path

class SimpleSentimentMonitor:
    def __init__(self, keywords=None):
        self.keywords = keywords or []
        self.results = {
            'hackernews': [],
            'wikipedia': [],
            'v2ex': [],
            'devto': [],
            'stackoverflow': [],
            'weibo': {'hot': []},
            'bilibili': {'hot': []},
            'xiaohongshu': {'search': []}
        }

    def run_opencli(self, command):
        """执行 opencli 命令"""
        try:
            result = subprocess.run(
                ['opencli'] + command,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # 尝试解析 JSON
                try:
                    return json.loads(result.stdout)
                except:
                    return result.stdout
            else:
                print(f"❌ 命令失败: {' '.join(command)}")
                return None
        except subprocess.TimeoutExpired:
            print(f"⏱️ 命令超时: {' '.join(command)}")
            return None
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            return None

    def monitor_hackernews(self):
        """监测 Hacker News"""
        print("\n📰 监测 Hacker News...")
        print("-" * 40)

        # 热门
        hot = self.run_opencli(['hackernews', 'top', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['hackernews'] = hot
            print(f"✅ Hacker News 热门: {len(hot)} 条")

        # 搜索
        if self.keywords:
            for keyword in self.keywords:
                search = self.run_opencli(['wikipedia', 'search', keyword, '--limit', '5', '--format', 'json'])
                if search:
                    self.results['wikipedia'].append({
                        'keyword': keyword,
                        'results': search
                    })
                    count = len(search) if isinstance(search, list) else 'N/A'
                    print(f"🔍 Wikipedia 搜索 [{keyword}]: {count} 条")

    def monitor_v2ex(self):
        """监测 V2EX"""
        print("\n🐧 监测 V2EX...")
        print("-" * 40)

        hot = self.run_opencli(['v2ex', 'hot', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['v2ex'] = hot
            print(f"✅ V2EX 热门: {len(hot)} 条")

    def monitor_devto(self):
        """监测 DEV.to"""
        print("\n💻 监测 DEV.to...")
        print("-" * 40)

        hot = self.run_opencli(['devto', 'top', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['devto'] = hot
            print(f"✅ DEV.to 热门: {len(hot)} 条")

    def monitor_stackoverflow(self):
        """监测 StackOverflow"""
        print("\n💻 监测 StackOverflow...")
        print("-" * 40)

        hot = self.run_opencli(['stackoverflow', 'hot', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['stackoverflow'] = hot
            print(f"✅ StackOverflow 热门: {len(hot)} 条")

    def monitor_weibo(self):
        """监测微博热搜"""
        print("\n🐦 监测微博热搜...")
        print("-" * 40)

        hot = self.run_opencli(['weibo', 'hot', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['weibo']['hot'] = hot
            print(f"✅ 微博热搜: {len(hot)} 条")

    def monitor_bilibili(self):
        """监测B站热门"""
        print("\n📺 监测B站热门...")
        print("-" * 40)

        hot = self.run_opencli(['bilibili', 'hot', '--limit', '10', '--format', 'json'])
        if hot:
            self.results['bilibili']['hot'] = hot
            print(f"✅ B站热门: {len(hot)} 条")

    def monitor_xiaohongshu(self):
        """监测小红书"""
        print("\n📕 监测小红书...")
        print("-" * 40)

        if self.keywords:
            for keyword in self.keywords:
                search = self.run_opencli(['xiaohongshu', 'search', keyword, '--limit', '5', '--format', 'json'])
                if search:
                    self.results['xiaohongshu']['search'].append({
                        'keyword': keyword,
                        'results': search
                    })
                    count = len(search) if isinstance(search, list) else 'N/A'
                    print(f"🔍 小红书搜索 [{keyword}]: {count} 条")

    def run(self, platforms=None):
        """运行监测"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print("=" * 50)
        print(f"📊 公开平台舆情监测报告")
        print(f"时间: {timestamp}")
        print(f"关键词: {', '.join(self.keywords) if self.keywords else '无'}")
        print("=" * 50)

        if not platforms or 'hackernews' in platforms:
            self.monitor_hackernews()
        if not platforms or 'v2ex' in platforms:
            self.monitor_v2ex()
        if not platforms or 'devto' in platforms:
            self.monitor_devto()
        if not platforms or 'stackoverflow' in platforms:
            self.monitor_stackoverflow()
        if not platforms or 'weibo' in platforms:
            self.monitor_weibo()
        if not platforms or 'bilibili' in platforms:
            self.monitor_bilibili()
        if not platforms or 'xiaohongshu' in platforms:
            self.monitor_xiaohongshu()

        self.save_report(timestamp)
        self.print_summary()

    def save_report(self, timestamp):
        """保存报告"""
        report_dir = Path(__file__).parent / 'reports'
        report_dir.mkdir(exist_ok=True)

        filename = f"simple-sentiment-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        filepath = report_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'keywords': self.keywords,
                'results': self.results
            }, f, ensure_ascii=False, indent=2)

        print(f"\n💾 报告已保存: {filepath}")

    def print_summary(self):
        """打印汇总"""
        print("\n" + "=" * 50)
        print("📈 监测汇总")
        print("=" * 50)

        print(f"📰 Hacker News: {len(self.results['hackernews'])} 条")
        print(f"📚 Wikipedia: {len(self.results['wikipedia'])} 次搜索")
        print(f"🐧 V2EX: {len(self.results['v2ex'])} 条")
        print(f"💻 DEV.to: {len(self.results['devto'])} 条")
        print(f"💻 StackOverflow: {len(self.results['stackoverflow'])} 条")
        print(f"🐦 微博热搜: {len(self.results['weibo']['hot'])} 条")
        print(f"📺 B站热门: {len(self.results['bilibili']['hot'])} 条")
        print(f"📕 小红书: {len(self.results['xiaohongshu']['search'])} 次搜索")

        print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description='公开平台舆情监测工具（无需 Browser Bridge）')
    parser.add_argument('-k', '--keywords', nargs='+', help='搜索关键词列表')
    parser.add_argument('-p', '--platforms', nargs='+',
                        choices=['hackernews', 'wikipedia', 'v2ex', 'devto', 'stackoverflow', 'weibo', 'bilibili', 'xiaohongshu'],
                        help='监测平台列表（默认：全部）')

    args = parser.parse_args()

    # 读取关键词
    keywords = args.keywords
    if not keywords:
        keywords_file = Path(__file__).parent / 'keywords.txt'
        if keywords_file.exists():
            with open(keywords_file, encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip()]

    if not keywords:
        print("⚠️ 未提供关键词，将只获取各平台热门内容")
        keywords = []

    monitor = SimpleSentimentMonitor(keywords=keywords)
    monitor.run(platforms=args.platforms)

if __name__ == '__main__':
    main()
