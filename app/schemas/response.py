from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class PageResponse(BaseModel, Generic[DataT]):
    """通用分页响应"""
    total: int = 0
    page: int = 1
    page_size: int = 20
    items: list[DataT] = []


class UploadResult(BaseModel):
    """上传导入结果"""
    batch_id: str = Field(description="上传批次标识")
    total_rows: int = Field(description="总行数")
    success_rows: int = Field(description="成功导入行数")
    failed_rows: int = Field(description="失败行数")
    failures: list[dict] = Field(default_factory=list, description="失败详情列表")


class LatestUploadDateResponse(BaseModel):
    """最大上传日期响应"""
    latest_upload_date: Optional[str] = Field(None, description="最大上传日期，格式 yyyy-MM-dd")


class APIResponse(BaseModel, Generic[DataT]):
    """统一响应格式"""
    code: int = 0
    message: str = "success"
    data: Optional[DataT] = None


def success(data: Any = None, message: str = "success") -> APIResponse[Any]:
    """构造成功响应"""
    return APIResponse[Any](code=0, message=message, data=data)


def error(code: int, message: str, data: Any = None) -> APIResponse[Any]:
    """构造错误响应"""
    return APIResponse[Any](code=code, message=message, data=data)
