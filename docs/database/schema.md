# 数据库设计

## 数据表总览

| 表名 | 说明 |
|------|------|
| `api_keys` | API Key 管理 |

## 表结构

### api_keys

API Key 信息表，用于存储客户端认证信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| app_id | VARCHAR(32) | UNIQUE, NOT NULL, INDEX | 应用标识（公钥） |
| app_name | VARCHAR(100) | NOT NULL | 应用名称 |
| client_secret | TEXT | NOT NULL | 客户端密钥（用于签名） |
| status | ENUM('active','disabled','expired') | NOT NULL, DEFAULT 'active' | 状态 |
| expires_at | DATETIME | NULLABLE | 过期时间 |
| description | VARCHAR(255) | NULLABLE | 描述 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW(), ON UPDATE NOW() | 更新时间 |

### 索引

| 表名 | 索引名 | 列 | 类型 |
|------|--------|-----|------|
| api_keys | ix_api_keys_app_id | app_id | UNIQUE |

## ER 图

```
┌──────────────────────────────────────┐
│              api_keys                 │
├──────────────────────────────────────┤
│ id (PK)           BIGINT             │
│ app_id (UQ, IX)   VARCHAR(32)        │
│ app_name          VARCHAR(100)       │
│ client_secret     TEXT               │
│ status            ENUM               │
│ expires_at        DATETIME           │
│ description       VARCHAR(255)       │
│ created_at        DATETIME           │
│ updated_at        DATETIME           │
└──────────────────────────────────────┘
```

## 数据库迁移

使用 Alembic 管理数据库迁移：

```bash
# 生成新的迁移脚本（需要 MySQL 运行中）
cd d:\Work\openapi-service
.venv\Scripts\alembic revision --autogenerate -m "description"

# 执行迁移
.venv\Scripts\alembic upgrade head

# 回滚迁移
.venv\Scripts\alembic downgrade -1
```
