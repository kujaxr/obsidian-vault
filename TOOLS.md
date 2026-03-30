# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### 高德地图
- AMAP_KEY: 20438ec00306928ebafa7113c3cac837

### OCR 文字识别
- 优先使用本地 OCR 技能：`~/.openclaw/skills/ocr-local-1.0.0/scripts/ocr.js`
- 命令：`node ~/.openclaw/skills/ocr-local-1.0.0/scripts/ocr.js <image> --lang chi_sim+eng`
- 备用：内置图像模型（识别效果更好但消耗更多 token）
- 本地 OCR 版本：tesseract.js v5.1.1（已降级修复 WASM bug）

### Cron 任务
| 任务 | 调度 | 推送 |
|------|------|------|
| GLaDOS 每日签到 | 每天 07:00 (Asia/Shanghai) | ✅ → Telegram (905207854) |

### NAS 推送
- （待补充：NAS 型号 / 推送服务配置）

### GitHub 推送
- （待补充：GitHub 仓库 / 推送事件类型 / 通知方式）
