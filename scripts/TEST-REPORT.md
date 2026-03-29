# 🚀 舆情监测测试报告

## 测试时间
2026-03-25 23:07

## 📦 准备工作

### ✅ 已完成
1. **脚本创建** - sentiment-monitor.py 和 sentiment-monitor.sh
2. **关键词配置** - keywords.txt
3. **使用文档** - README.md
4. **脚本权限** - sentiment-monitor.sh 已设置执行权限

### ⏳ 进行中
1. **OpenCLI 安装** - `npm install -g @jackwener/opencli`
   - 状态: 正在安装...
   - 预计时间: 1-3 分钟

## 🎯 下一步测试计划

### 测试一：基础功能测试
```bash
# 测试 B站热榜（公开 API，无需登录）
opencli bilibili hot --limit 5
```

### 测试二：关键词搜索
```bash
# 测试多平台搜索
python3 /Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.py \
  -k 测试关键词 \
  -p bilibili xiaohongshu weibo
```

### 测试三：完整监测流程
```bash
# 使用配置文件中的关键词
python3 /Users/rayxu/.openclaw/workspace/scripts/sentiment-monitor.py
```

## ⚠️ 当前限制

1. **Browser Bridge 扩展**
   - 需要在 Chrome 中安装
   - 对于 B站/抖音/小红书/微博，需要登录状态

2. **API 限制**
   - 某些平台可能有请求频率限制
   - 建议：间隔 ≥ 30 分钟

## 📊 预期输出

```
==================================
📊 舆情监测报告 - 2026-03-25 23:10:00
关键词: iPhone 小米汽车
==================================

📺 B站 (Bilibili)
----------------------------------------
❌ B站热榜获取失败
🔍 B站搜索: iPhone
[视频列表...]
...
```

## 💡 临时替代方案

在 OpenCLI 安装完成前，可以使用：

1. **直接浏览器访问**
   - B站热搜: https://www.bilibili.com/v/popular/all
   - 微博热搜: https://s.weibo.com/top/summary
   - 抖音热榜: https://www.douyin.com

2. **使用其他工具**
   - 如果有 curl，可以直接调用 API
   - 使用 Puppeteer/Playwright 做自动化

## 🔍 故障排查

### 如果 opencli 安装失败
```bash
# 检查 npm 版本
npm --version  # 需要 >= 8.x

# 清理缓存后重试
npm cache clean --force
npm install -g @jackwener/opencli

# 检查安装位置
which opencli

# 手动测试
opencli list --limit 1
```

### 如果扩展未连接
```bash
# 诊断命令
opencli doctor

# 检查 Chrome 扩展
# 1. 打开 chrome://extensions
# 2. 确认 opencli Browser Bridge 已启用
# 3. 刷新页面
```

---

**更新时间**: 2026-03-25 23:10
**状态**: 等待 OpenCLI 安装完成
