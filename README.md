# OpenAPI Service

基于 **Python FastAPI** 构建的对外 API 服务平台，提供安全、稳定、高效的接口服务。

## 技术栈

| 组件 | 选型 |
|------|------|
| 语言框架 | Python 3.13 + FastAPI |
| 虚拟环境 | uv |
| 数据库 | MySQL 8.0+ |
| ORM | SQLAlchemy 2.0 (异步引擎) |
| 数据校验 | Pydantic v2 |
| 数据库迁移 | Alembic (异步) |
| 接口认证 | API Key + HMAC-SHA256 签名 |

## 快速开始

### 前置条件

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- MySQL 8.0+

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置环境变量

```bash
copy .env.example .env
```

编辑 `.env` 文件，配置数据库连接信息。

### 3. 创建数据库

```sql
CREATE DATABASE IF NOT EXISTS openapi_service CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 执行数据库迁移

```bash
.venv\Scripts\alembic upgrade head
```

### 5. 启动服务

```bash
.venv\Scripts\uvicorn app.main:app --reload
```

访问 http://localhost:8000/api/v1/docs 查看 Swagger 文档。

## 项目结构

```
openapi-service/
├── app/               # 应用主代码
│   ├── main.py       # 应用入口
│   ├── config.py     # 配置管理
│   ├── database.py   # 数据库引擎
│   ├── api/          # API 路由
│   ├── models/       # ORM 模型
│   ├── schemas/      # 数据校验
│   ├── services/     # 业务逻辑
│   ├── core/         # 基础设施
│   └── utils/        # 工具函数
├── alembic/          # 数据库迁移
├── docs/             # 项目文档
└── pyproject.toml    # 依赖配置
```

## 接口认证

本服务使用 **API Key + HMAC-SHA256 签名** 进行认证。

1. 调用 `POST /api/v1/auth/apply` 申请 API Key
2. 请求时携带 `X-App-ID`、`X-Timestamp`、`X-Nonce`、`X-Signature` 四个 Header
3. 服务端验证签名、时间窗口和 Nonce 防重放

详细认证说明请参考 [docs/api/authentication.md](docs/api/authentication.md)。

## API 路由

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `GET` | `/api/v1/health` | 健康检查 | 否 |
| `POST` | `/api/v1/auth/apply` | 申请 API Key | 否 |
| `GET` | `/api/v1/auth/keys` | 查看 API Key 列表 | 是 |
| `POST` | `/api/v1/auth/revoke` | 撤销 API Key | 是 |

## 文档

项目文档按类型分类存放在 `docs/` 目录下：

- [架构总览](docs/architecture/overview.md)
- [接口认证说明](docs/api/authentication.md)
- [错误码说明](docs/api/error-codes.md)
- [数据库设计](docs/database/schema.md)
- [部署指南](docs/deployment/setup.md)
- [环境变量说明](docs/deployment/env-config.md)

## 统一响应格式

所有接口统一返回格式：

```json
{
  "code": 0,
  "message": "success",
  "data": null
}
```
