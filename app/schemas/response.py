from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    """统一响应格式"""
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None


def success(data: Any = None, message: str = "success") -> APIResponse:
    """构造成功响应"""
    return APIResponse(code=0, message=message, data=data)


def error(code: int, message: str, data: Any = None) -> APIResponse:
    """构造错误响应"""
    return APIResponse(code=code, message=message, data=data)
