# 限流说明

> 当前版本暂未实现限流功能，此文档为限流设计规划。

## 限流策略（规划中）

### 方案：基于 API Key 的限流

根据每个 API Key 的 `rate_limit` 配置进行限流：

- **维度**：按 API Key（app_id）进行限流
- **窗口**：滑动时间窗口，例如 1 分钟
- **上限**：每个 API Key 每分钟最多请求 N 次
- **响应**：超出限制返回 HTTP 429

### 超出限流的响应

```json
{
  "code": 42900,
  "message": "Rate limit exceeded. Please try again later.",
  "data": null
}
```

### 实现方式

- 开发环境：使用内存缓存（当前 nonce 缓存的基础上升级）
- 生产环境：建议使用 Redis

### 请求头反馈

限流相关的响应头（规划中）：

| Header | 说明 |
|--------|------|
| `X-RateLimit-Limit` | 时间窗口内的总请求上限 |
| `X-RateLimit-Remaining` | 当前窗口剩余请求次数 |
| `X-RateLimit-Reset` | 窗口重置的 Unix 时间戳 |
