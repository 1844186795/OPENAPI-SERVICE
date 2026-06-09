"""API Key 模型"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ApiKey(BaseModel):
    """API Key 信息表"""
    __tablename__ = "api_keys"
    __table_args__ = {"comment": "API Key 信息表"}

    app_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True, comment="应用标识（公钥）")
    app_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="应用名称")
    client_secret: Mapped[str] = mapped_column(Text, nullable=False, comment="客户端密钥（用于HMAC签名）")
    status: Mapped[str] = mapped_column(Enum("active", "disabled", "expired"), default="active", nullable=False, comment="状态：active-启用，disabled-禁用，expired-已过期")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="过期时间")
    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="描述信息")


def generate_app_id() -> str:
    """生成应用ID"""
    return "ak_" + uuid.uuid4().hex[:28]


def generate_client_secret() -> str:
    """生成客户端密钥"""
    return "sk_" + uuid.uuid4().hex + uuid.uuid4().hex[:16]
