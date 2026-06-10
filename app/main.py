import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.core.exceptions.handlers import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.api.v1.auth import router as auth_router
from app.core.middleware.logging import RequestLoggingMiddleware
from app.schemas.response import success

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openapi-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("正在启动 %s...", settings.APP_NAME)
    yield
    logger.info("正在关闭 %s...", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    root_path=settings.ROOT_PATH,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan,
)

# --- 注册异常处理器 ---
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# --- 注册路由 ---
app.include_router(auth_router, prefix="/api/v1")

# --- 注册中间件 ---
app.add_middleware(RequestLoggingMiddleware)


@app.get("/")
async def root():
    return success(message="OpenAPI Service is running")


@app.get("/api/v1/health")
async def health_check():
    return success(message="OK")
