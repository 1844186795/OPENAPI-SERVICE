from fastapi import Depends, Header, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions.handlers import AuthenticationError, PermissionDenied, ApiKeyExpiredError
from app.core.security.auth import verify_signature
from app.database import get_db
from app.models.api_key import ApiKey
import time


async def get_api_key_by_app_id(db: AsyncSession, app_id: str) -> ApiKey | None:
    """根据应用ID查询 API Key"""
    result = await db.execute(select(ApiKey).where(ApiKey.app_id == app_id))
    return result.scalar_one_or_none()


async def require_auth(
    request: Request,
    x_app_id: str = Header(..., alias="X-App-ID"),
    x_signature: str = Header(..., alias="X-Signature"),
    x_timestamp: str = Header(..., alias="X-Timestamp"),
    x_nonce: str = Header(..., alias="X-Nonce"),
    db: AsyncSession = Depends(get_db),
) -> ApiKey:
    """API Key 认证依赖注入，保护需要认证的路由"""
    if not x_app_id or not x_signature or not x_timestamp or not x_nonce:
        raise AuthenticationError("缺少认证请求头")

    api_key = await get_api_key_by_app_id(db, x_app_id)
    if not api_key:
        raise AuthenticationError("无效的 API Key")

    # 检查是否过期，若过期则同步更新状态
    if api_key.expires_at and time.time() > api_key.expires_at.timestamp():
        api_key.status = "expired"
        db.add(api_key)
        await db.flush()
        raise ApiKeyExpiredError()

    body = None
    if request.method in ("POST", "PUT", "PATCH"):
        body_bytes = await request.body()
        if body_bytes:
            body = body_bytes.decode("utf-8")

    verify_signature(
        api_key=api_key,
        signature=x_signature,
        timestamp=x_timestamp,
        nonce=x_nonce,
        method=request.method,
        path=request.url.path,
        body=body,
    )

    return api_key


async def require_admin(
    x_admin_key: str = Header(..., alias="X-Admin-Key"),
) -> None:
    """管理员主密钥认证依赖注入，保护 API Key 管理接口"""
    if not x_admin_key:
        raise PermissionDenied("缺少管理员密钥")
    if x_admin_key != settings.ADMIN_API_KEY:
        raise PermissionDenied("无效的管理员密钥")
    return None


async def require_auth_simple(
    request: Request,
    x_app_id: str = Header(..., alias="X-App-ID"),
    x_signature: str = Header(..., alias="X-Signature"),
    x_timestamp: str = Header(..., alias="X-Timestamp"),
    x_nonce: str = Header(..., alias="X-Nonce"),
    db: AsyncSession = Depends(get_db),
) -> ApiKey:
    """API Key 认证依赖注入（不校验请求体，适用于文件上传等场景）"""
    if not x_app_id or not x_signature or not x_timestamp or not x_nonce:
        raise AuthenticationError("缺少认证请求头")

    api_key = await get_api_key_by_app_id(db, x_app_id)
    if not api_key:
        raise AuthenticationError("无效的 API Key")

    # 检查是否过期，若过期则同步更新状态
    if api_key.expires_at and time.time() > api_key.expires_at.timestamp():
        api_key.status = "expired"
        db.add(api_key)
        await db.flush()
        raise ApiKeyExpiredError()

    # 校验签名但不读取 body（文件上传场景 body 为二进制数据）
    verify_signature(
        api_key=api_key,
        signature=x_signature,
        timestamp=x_timestamp,
        nonce=x_nonce,
        method=request.method,
        path=request.url.path,
        body=None,
    )

    return api_key
