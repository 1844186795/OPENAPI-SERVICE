from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ApiKeyCreateRequest(BaseModel):
    app_name: str = Field(..., min_length=1, max_length=100, description="应用名称")
    description: Optional[str] = Field(None, max_length=255, description="描述信息")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class ApiKeyCreateResponse(BaseModel):
    app_id: str = Field(description="应用标识（公钥）")
    app_name: str = Field(description="应用名称")
    client_secret: str = Field(description="客户端密钥（用于HMAC签名）")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class ApiKeyInfo(BaseModel):
    app_id: str = Field(description="应用标识（公钥）")
    app_name: str = Field(description="应用名称")
    status: str = Field(description="状态：active-启用，disabled-禁用，expired-已过期")
    description: Optional[str] = Field(None, description="描述信息")
    expires_at: Optional[datetime] = Field(None, description="过期时间")
    created_at: datetime = Field(description="创建时间")


class ApiKeyListResponse(BaseModel):
    total: int = Field(description="API Key 总数")
    items: list[ApiKeyInfo] = Field(description="API Key 列表")
