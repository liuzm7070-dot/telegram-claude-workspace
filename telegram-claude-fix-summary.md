# 2026-06-19: Telegram ↔ Claude Code 通信修复总结

## 背景
用户希望通过 Telegram 与 Claude Code 会话通信，实现移动端使用。

## 问题与修复

### 1. ⏱️ proxychains4 超时 (15s → 120s)
**问题**: `/etc/proxychains4.conf` 中 `tcp_read_time_out` 为 15 秒，而 Telegram Bot API 的 `getUpdates` 长轮询需要 30+ 秒。代理在消息到达前切断连接。
**修复**: 修改 `tcp_read_time_out` 为 120000 毫秒（120秒）。

### 2. 📦 MCP SDK 版本升级 (1.27.1 → 1.29.0)
**问题**: Telegram 插件使用的 MCP SDK 版本较旧，与 WeChat 插件（1.29.0）不一致。
**修复**: `bun install @modelcontextprotocol/sdk@1.29.0`

### 3. 🔌 proxychains4 → bun 直连
**问题**: `proxychains4` 的 LD_PRELOAD 可能干扰 MCP stdout 通信，影响 channel 通知。
**修复**: `.mcp.json` 从 `proxychains4 -q bun ...` 改为 `bun run ...`，代理通过 `.env` 环境变量 (`HTTP_PROXY`/`HTTPS_PROXY`) 处理。

### 4. 📨 read_inbox 消息队列
**问题**: `notifications/claude/channel` 通知系统存在未知 bug，消息虽能到达 Telegram 并被 MCP 消费，但通知无法在 Claude 会话中显示为 `<channel>` 标签。
**解决**: 在 `server.ts` 中添加：
- `INBOX_FILE` 消息队列（每次收到消息写入 JSONL 文件）
- `read_inbox` MCP 工具（读取并清空消息队列）

### 5. 🔔 轮询机制
使用 `/loop 60s` 每分钟调用 `read_inbox` 检查新消息。

## 当前架构

```
Telegram App
    ↕ Telegram Bot API
MCP Server (bun, HTTP_PROXY)
    ↕ MCP stdio
Claude Code Session
    ↕ read_inbox 轮询
Claude AI 响应
```

## 修改的文件
- `/etc/proxychains4.conf` — tcp_read_time_out: 15000 → 120000
- `~/.claude/.../telegram/0.0.6/server.ts` — +read_inbox 工具, +inbox 队列
- `~/.claude/.../telegram/0.0.6/.mcp.json` — proxychains4 → bun
- `~/.claude/.../telegram/0.0.6/node_modules/@modelcontextprotocol/sdk` — 1.29.0

## 遗留问题
- `notifications/claude/channel` 通知在 DeepSeek API 后端下无法触发 `<channel>` 标签（可能为 Claude Code harness 兼容性 bug）
- 需 `read_inbox` 轮询作为变通方案
