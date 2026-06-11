from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.handlers import BusinessError
from app.core.security.deps import require_admin
from app.database import get_db
from app.schemas.api_key import ApiKeyCreateRequest, ApiKeyCreateResponse, ApiKeyInfo, ApiKeyListResponse
from app.schemas.response import APIResponse, success
from app.services import api_key as api_key_service

router = APIRouter(prefix="/auth", tags=["认证中心"])


@router.post("/apply", response_model=APIResponse[ApiKeyCreateResponse], summary="申请 API Key",
             description="创建一个新的 API Key，返回 app_id 和 client_secret，client_secret 只会在创建时显示一次，请妥善保存。需要携带管理员密钥进行身份认证。",
             response_description="申请成功返回 app_id 和 client_secret，data 结构见 ApiKeyCreateResponse")
async def apply_api_key(
    req: ApiKeyCreateRequest,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_admin),
):
    """申请新的 API Key（需要管理员密钥）"""
    if req.expires_at:
        from datetime import datetime, timezone

        expires_at = req.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            raise BusinessError(code=40000, message="Expiration time must be in the future")

    api_key = await api_key_service.create_api_key(
        db=db,
        app_name=req.app_name,
        description=req.description,
        expires_at=req.expires_at,
    )

    return success(
        data=ApiKeyCreateResponse(
            app_id=api_key.app_id,
            app_name=api_key.app_name,
            client_secret=api_key.client_secret,
            expires_at=api_key.expires_at,
        ).model_dump(),
        message="API Key created successfully. Please save the client_secret as it will not be shown again.",
    )


@router.get("/keys", response_model=APIResponse[ApiKeyListResponse], summary="获取 API Key 列表",
            description="获取所有已申请的 API Key 列表，需要携带管理员密钥进行身份认证。",
            response_description="返回 API Key 列表，data 结构见 ApiKeyListResponse")
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_admin),
):
    """获取 API Key 列表（需要管理员密钥）"""
    items, total = await api_key_service.get_api_key_list(db)

    return success(
        data=ApiKeyListResponse(
            total=total,
            items=[
                ApiKeyInfo(
                    app_id=item.app_id,
                    app_name=item.app_name,
                    status=item.status,
                    description=item.description,
                    expires_at=item.expires_at,
                    created_at=item.created_at,
                )
                for item in items
            ],
        ).model_dump()
    )


@router.post("/revoke", response_model=APIResponse[None], summary="撤销 API Key",
             description="根据 app_id 撤销指定的 API Key，撤销后该 Key 将无法继续使用。需要携带管理员密钥进行身份认证。",
             response_description="撤销成功仅返回 message，无 data 内容")
async def revoke_api_key(
    app_id: str = Query(..., description="要撤销的应用标识（app_id）"),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_admin),
):
    """撤销 API Key（需要管理员密钥）"""
    await api_key_service.revoke_api_key(db, app_id)
    return success(message="API Key has been revoked")
