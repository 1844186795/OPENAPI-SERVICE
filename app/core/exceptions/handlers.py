from typing import Any, Optional

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.response import error


class AppException(Exception):
    """应用异常基类"""

    def __init__(self, code: int = 50000, message: str = "Internal server error", data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(self.message)


class AuthenticationError(AppException):
    """认证失败异常"""

    def __init__(self, message: str = "认证失败", data: Any = None):
        super().__init__(code=40100, message=message, data=data)


class InvalidSignatureError(AppException):
    """签名无效异常"""

    def __init__(self, message: str = "签名无效", data: Any = None):
        super().__init__(code=40101, message=message, data=data)


class ApiKeyExpiredError(AppException):
    """API Key 过期异常"""

    def __init__(self, message: str = "API Key 已过期", data: Any = None):
        super().__init__(code=40102, message=message, data=data)


class PermissionDenied(AppException):
    """权限不足异常"""

    def __init__(self, message: str = "权限不足", data: Any = None):
        super().__init__(code=40300, message=message, data=data)


class NotFoundError(AppException):
    """资源不存在异常"""

    def __init__(self, message: str = "资源不存在", data: Any = None):
        super().__init__(code=40400, message=message, data=data)


class RateLimitError(AppException):
    """请求频率超限异常"""

    def __init__(self, message: str = "请求过于频繁，请稍后重试", data: Any = None):
        super().__init__(code=42900, message=message, data=data)


class BusinessError(AppException):
    """业务逻辑异常"""

    def __init__(self, code: int = 40000, message: str = "业务错误", data: Any = None):
        super().__init__(code=code, message=message, data=data)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.code // 100,
        content=error(code=exc.code, message=exc.message, data=exc.data).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=error(code=42200, message="Validation error", data=exc.errors()).model_dump(),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error(code=exc.status_code * 100, message=str(exc.detail)).model_dump(),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error(code=50000, message="Internal server error").model_dump(),
    )
