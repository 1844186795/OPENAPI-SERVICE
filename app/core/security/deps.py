from fastapi import Depends, Header, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.handlers import AuthenticationError, InvalidSignatureError
from app.core.security.auth import verify_signature
from app.database import get_db
from app.models.api_key import ApiKey


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
