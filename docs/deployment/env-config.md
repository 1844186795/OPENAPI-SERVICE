# 环境变量说明

## 配置方式

项目使用 `pydantic-settings` 从 `.env` 文件加载配置。配置文件优先级：

1. 环境变量（最高优先级）
2. `.env` 文件（推荐方式）

## 环境变量清单

### 应用配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `APP_NAME` | `OpenAPI Service` | 应用名称，显示在 OpenAPI 文档标题 |
| `APP_DEBUG` | `true` | 调试模式，开启时输出 SQL 日志 |
| `APP_HOST` | `0.0.0.0` | 服务监听地址 |
| `APP_PORT` | `8000` | 服务监听端口 |
| `ROOT_PATH` | `` | 反向代理路径前缀（如 `/openapi`），空字符串表示无前缀 |

### 数据库配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `MYSQL_HOST` | `localhost` | MySQL 主机地址 |
| `MYSQL_PORT` | `3306` | MySQL 端口 |
| `MYSQL_USER` | `root` | MySQL 用户名 |
| `MYSQL_PASSWORD` | `` | MySQL 密码 |
| `MYSQL_DATABASE` | `openapi_service` | MySQL 数据库名 |

## 示例 .env 文件

```ini
# ============================
# Application Configuration
# ============================
APP_NAME=OpenAPI Service
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000

# ============================
# Database Configuration
# ============================
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=openapi_service
```

## 注意事项

1. `.env` 文件包含敏感信息（数据库密码），**不要提交到版本控制**
2. 所有新成员应从 `.env.example` 复制并修改为自己的配置
3. 生产环境建议通过系统环境变量设置，而不是 `.env` 文件
