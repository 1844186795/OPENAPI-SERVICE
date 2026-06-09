# 部署指南

## 环境要求

- Python 3.12+
- uv（Python 虚拟环境和依赖管理工具）
- MySQL 8.0+

## 快速开始

### 1. 克隆项目

```bash
cd d:\Work\openapi-service
```

### 2. 配置环境变量

复制环境变量模板并根据实际情况修改：

```bash
copy .env.example .env
```

编辑 `.env` 文件，配置 MySQL 连接信息：

```ini
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=openapi_service
```

### 3. 安装依赖

```bash
uv sync
```

### 4. 创建数据库

连接到 MySQL 并创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS openapi_service CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 执行数据库迁移

```bash
.venv\Scripts\alembic upgrade head
```

### 6. 启动服务

```bash
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. 验证服务

```bash
curl http://localhost:8000/api/v1/health
```

## API 文档

启动服务后访问：

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 生产部署建议

### 使用 Gunicorn + Uvicorn Workers

```bash
.venv\Scripts\pip install gunicorn
.venv\Scripts\gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 环境变量

生产环境建议设置：

```ini
APP_DEBUG=false
```

### 日志

日志输出到控制台，生产环境建议配置日志收集系统。
