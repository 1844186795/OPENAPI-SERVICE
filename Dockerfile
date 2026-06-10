# ============================================================
# Stage 1: 依赖构建阶段
# 使用 uv 工具安装 Python 依赖，生成虚拟环境
# ============================================================
FROM python:3.13-slim AS builder

# 安装 uv 包管理工具
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 使用中科大 PyPI 镜像源加速依赖下载
# 如果镜像源不可用，可删除 --index-url 参数回退到官方源
ENV UV_INDEX_URL=https://mirrors.ustc.edu.cn/pypi/web/simple/

# 先复制依赖清单，利用 Docker 层缓存加速重复构建
COPY pyproject.toml uv.lock ./

# 仅安装生产环境依赖（不安装开发依赖）
# 注意：显式传递 UV_INDEX_URL 环境变量给 uv build 步骤使用
RUN UV_INDEX_URL=https://mirrors.ustc.edu.cn/pypi/web/simple/ uv sync --frozen --no-dev


# ============================================================
# Stage 2: 运行阶段
# 基于精简镜像，仅复制构建产物和应用代码
# ============================================================
FROM python:3.13-slim

WORKDIR /app

# 设置时区为中国时区
ENV TZ=Asia/Shanghai

# 从构建阶段复制已安装好的虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 复制应用源码
COPY app/ ./app/
# 复制数据库迁移配置和脚本
COPY alembic.ini .
COPY alembic/ ./alembic/

# 将虚拟环境加入 PATH，确保直接使用 python 命令
ENV PATH="/app/.venv/bin:${PATH}"

# 应用监听端口
EXPOSE 8001

# 使用 uvicorn 启动 FastAPI 应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]