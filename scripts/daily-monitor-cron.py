#!/usr/bin/env python3
"""
文献监控定时任务脚本 - 每天早上6:10
通过Telegram Bot发送简报
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置
SCRIPT_DIR = Path("/Users/rayxu/.openclaw/workspace/scripts")
VENV_PYTHON = SCRIPT_DIR / "literature_env" / "bin" / "python3"
LOG_FILE = SCRIPT_DIR / "literature-cron.log"
BOT_TOKEN = "8132195706:AAHDfR05pmH7Z_-Dv_3MmFC6PCkJXHhR4mI"
TELEGRAM_TARGET = "905207854"


def log(message: str):
    """日志记录"""
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


def run_literature_monitor():
    """运行文献监控"""
    log("开始文献监控...")

    try:
        result = subprocess.run(
            [str(VENV_PYTHON), str(SCRIPT_DIR / "literature-monitor.py")],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0:
            log("✅ 文献监控完成")
            return True
        else:
            log(f"❌ 文献监控失败")
            return False

    except Exception as e:
        log(f"❌ 文献监控出错: {e}")
        return False


def load_brief(filepath: Path) -> str:
    """读取简报文件"""
    if filepath and filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def main():
    """主函数"""
    log("=" * 60)
    log("📚 文献监控定时任务开始")
    log("=" * 60)

    # 1. 运行文献监控
    literature_ok = run_literature_monitor()

    # 2. 读取简报
    log("读取简报...")
    literature_briefs = sorted((SCRIPT_DIR / "literature").glob("literature-brief-*.txt"), reverse=True)
    literature_brief = load_brief(literature_briefs[0] if literature_briefs else None)

    # 3. 构建并发送消息
    if literature_ok and literature_brief:
        lines = literature_brief.strip().split("\n")
        content_lines = []
        skip_next = True
        for line in lines:
            if line.startswith("📚 文献监控简报"):
                continue
            if skip_next and line.startswith("="):
                skip_next = False
                continue
            content_lines.append(line)

        messages = []
        messages.append("📚 <b>文献监控简报</b>")
        messages.append("\n".join(content_lines[:35]))  # 限制行数

        full_message = "\n".join(messages)

        # Telegram消息有4096字符限制
        if len(full_message) > 4000:
            full_message = full_message[:4000] + "\n...(内容过长已截断)"

        send_telegram(full_message)
    else:
        log("⚠️ 没有生成文献简报")

    log("=" * 60)
    log("📚 文献监控定时任务完成")
    log("=" * 60)


if __name__ == "__main__":
    sys.exit(main())
