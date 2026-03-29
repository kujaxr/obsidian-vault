# 舆情监测工具使用指南

## 📋 前置条件

### 1. 安装 opencli
```bash
npm install -g @jackwener/opencli
```

### 2. 安装 Browser Bridge 扩展
1. 打开 Chrome 浏览器
2. 访问 `chrome://extensions`
3. 启用"开发者模式"（右上角）
4. 点击"加载已解压的扩展程序"
5. 选择 opencli 的 `extension/` 文件夹

### 3. 在 Chrome 中登录各平台
- B站 (bilibili.com)
- 抖音 (douyin.com 或 tiktok.com)
- 小红书 (xiaohongshu.com)
- 微博 (weibo.com)

---

## 🚀 使用方法

### 方法一：Shell 脚本（简单快速）

```bash
# 赋予执行权限
chmod +x /Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.sh

# 运行（搜索关键词）
/Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.sh "iPhone"

# 或运行（获取各平台热门）
/Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.sh
```

**输出示例：**
```
===================================
📊 舆情监测报告 - 2026-03-25 23:00:00
关键词: iPhone
===================================

📺 B站 (Bilibili)
---
🔍 B站搜索: iPhone
[视频列表...]
```

---

### 方法二：Python 脚本（功能完整）

#### 基础使用

```bash
# 进入脚本目录
cd /Users/rayxu/.openclaw/workspace/scripts

# 查看帮助
python3 sentiment-monitor.py --help

# 只获取各平台热门（无关键词）
python3 sentiment-monitor.py

# 指定关键词
python3 sentiment-monitor.py -k iPhone 小米汽车

# 指定平台
python3 sentiment-monitor.py -p bilibili weibo

# 只显示汇总统计
python3 sentiment-monitor.py --summary
```

#### 高级用法

```bash
# 组合使用
python3 sentiment-monitor.py -k iPhone AI -p bilibili xiaohongshu --summary
```

**参数说明：**
- `-k, --keywords`：搜索关键词（多个）
- `-p, --platforms`：指定平台（bilibili, tiktok, xiaohongshu, weibo）
- `--summary`：只显示汇总统计

---

## 📊 输出说明

### Python 脚本输出

1. **终端输出**
   - 实时显示各平台获取结果
   - 最后显示汇总统计

2. **JSON 报告文件**
   - 保存到 `reports/` 目录
   - 文件名格式：`sentiment-report-YYYYMMDD-HHMMSS.json`
   - 包含完整数据结构

**报告示例：**
```json
{
  "timestamp": "2026-03-25 23:00:00",
  "keywords": ["iPhone", "小米汽车"],
  "results": {
    "bilibili": {
      "hot": [...],
      "search": [
        {"keyword": "iPhone", "results": [...]},
        {"keyword": "小米汽车", "results": [...]}
      ]
    },
    "tiktok": {
      "explore": [...],
      "search": [...]
    },
    "xiaohongshu": {
      "feed": [...],
      "search": [...]
    },
    "weibo": {
      "hot": [...],
      "search": [...]
    }
  }
}
```

---

## ⏰ 定时监测设置

### 方案一：Cron（Linux/macOS）

```bash
# 编辑 crontab
crontab -e

# 每小时监测一次
0 * * * * cd /Users/rayxu/.openclaw/workspace/scripts && python3 sentiment-monitor.py -k iPhone 小米汽车 >> /var/log/sentiment-monitor.log 2>&1

# 每 30 分钟监测一次
*/30 * * * * cd /Users/rayxu/.openclaw/workspace/scripts && python3 sentiment-monitor.py -k iPhone 小米汽车 >> /var/log/sentiment-monitor.log 2>&1

# 每天早上 8 点监测
0 8 * * * cd /Users/rayxu/.openclaw/workspace/scripts && python3 sentiment-monitor.py -k iPhone 小米汽车 >> /var/log/sentiment-monitor.log 2>&1
```

### 方案二：launchd（macOS 推荐）

创建 `~/Library/LaunchAgents/com.sentiment.monitor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sentiment.monitor</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.py</string>
        <string>-k</string>
        <string>iPhone</string>
        <string>小米汽车</string>
        <string>--summary</string>
    </array>

    <key>StartInterval</key>
    <integer>3600</integer>  <!-- 每小时执行一次 -->

    <key>StandardOutPath</key>
    <string>/Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.err</string>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

加载任务：
```bash
launchctl load ~/Library/LaunchAgents/com.sentiment.monitor.plist
launchctl start com.sentiment.monitor
```

---

## 🔧 自定义关键词

编辑 `keywords.txt` 文件：
```bash
vim /Users/rayxu/.openclaw/workspace/scripts/keywords.txt
```

每行一个关键词，支持：
- 品牌名
- 产品名
- 事件名
- 行业关键词

---

## 📈 数据分析建议

### 1. 热度趋势分析
```python
import json
from pathlib import Path

# 读取多次监测报告
reports = sorted(Path('reports').glob('sentiment-report-*.json'))

for report in reports:
    with open(report) as f:
        data = json.load(f)
        # 统计各平台搜索结果数
        # 绘制趋势图
```

### 2. 情感分析（需要额外工具）
- 使用 NLP 库分析评论情感
- 统计正面/负面/中性占比
- 生成情感趋势图

### 3. 关键词云
```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 生成关键词云
text = ' '.join(all_titles)
wordcloud = WordCloud(font_path='SimHei.ttf').generate(text)
plt.imshow(wordcloud)
plt.show()
```

---

## ⚠️ 注意事项

1. **登录状态**
   - 必须在 Chrome 中登录各平台
   - 登录状态会过期，需定期刷新

2. **频率限制**
   - 避免过于频繁的请求
   - 建议间隔 ≥ 30 分钟

3. **数据准确性**
   - B站热搜 = 实时热门
   - 抖音搜索 = 可能有限流
   - 小红书 = 部分内容需要登录
   - 微博 = 搜索可能受账号限制

4. **错误处理**
   - 检查 `*.log` 和 `*.err` 文件
   - 确保网络连接正常
   - 定期重启 Chrome 清理缓存

---

## 🚀 进阶优化

### 1. 多关键词并行监测
```python
# 修改脚本，使用多线程/协程
# 同时搜索多个关键词
```

### 2. 历史数据存储
```python
# 将数据存入数据库（SQLite/PostgreSQL）
# 支持历史查询和趋势分析
```

### 3. 告警机制
```python
# 检测到异常热度或负面舆情时
# 发送 Telegram/邮件通知
```

### 4. 可视化仪表板
```python
# 使用 Streamlit/Plotly 创建实时仪表板
# 展示趋势图、热词云、情感分析
```

---

## 📞 问题排查

### 问题：`Extension not connected`
**解决：**
1. 确保 Chrome 正在运行
2. 检查扩展是否已启用
3. 重启扩展：`chrome://extensions`

### 问题：登录状态失效
**解决：**
1. 在 Chrome 中重新登录各平台
2. 清理 Cookie 后重启 Chrome

### 问题：搜索结果为空
**解决：**
1. 检查关键词是否正确
2. 确认该平台有相关内容
3. 尝试使用热门关键词测试

---

## 🎯 下一步

1. ✅ 安装 Browser Bridge 扩展
2. ✅ 在 Chrome 中登录 B站、抖音、小红书、微博
3. ✅ 测试脚本：`python3 sentiment-monitor.py -k 测试`
4. ✅ 配置定时任务（launchd 或 cron）
5. ✅ 分析历史数据，优化监测策略

---

**需要帮助？运行 `python3 sentiment-monitor.py --help` 查看完整参数说明！**
