from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.handlers import BusinessError
from app.models.api_key import ApiKey, generate_app_id, generate_client_secret


async def create_api_key(
    db: AsyncSession,
    app_name: str,
    description: Optional[str] = None,
    expires_at: Optional[datetime] = None,
) -> ApiKey:
    """创建新的 API Key"""
    api_key = ApiKey(
        app_id=generate_app_id(),
        app_name=app_name,
        client_secret=generate_client_secret(),
        description=description,
        expires_at=expires_at,
    )
    db.add(api_key)
    await db.flush()
    return api_key


async def get_api_key_list(db: AsyncSession) -> tuple[list[ApiKey], int]:
    """获取所有 API Key 列表"""
    result = await db.execute(select(ApiKey).order_by(ApiKey.created_at.desc()))
    items = list(result.scalars().all())
    return items, len(items)


async def revoke_api_key(db: AsyncSession, app_id: str) -> None:
    """撤销（禁用）API Key"""
    result = await db.execute(select(ApiKey).where(ApiKey.app_id == app_id))
    api_key = result.scalar_one_or_none()
    if not api_key:
        raise BusinessError(code=40400, message="API Key 不存在")
    api_key.status = "disabled"
    await db.flush()
