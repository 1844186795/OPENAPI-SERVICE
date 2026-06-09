from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ApiKeyCreateRequest(BaseModel):
    app_name: str = Field(..., min_length=1, max_length=100, description="应用名称")
    description: Optional[str] = Field(None, max_length=255, description="描述信息")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class ApiKeyCreateResponse(BaseModel):
    app_id: str
    app_name: str
    client_secret: str
    expires_at: Optional[datetime]


class ApiKeyInfo(BaseModel):
    app_id: str
    app_name: str
    status: str
    description: Optional[str]
    expires_at: Optional[datetime]
    created_at: datetime


class ApiKeyListResponse(BaseModel):
    total: int
    items: list[ApiKeyInfo]
