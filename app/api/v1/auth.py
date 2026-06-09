from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.handlers import BusinessError
from app.core.security.deps import require_auth
from app.database import get_db
from app.models.api_key import ApiKey
from app.schemas.api_key import ApiKeyCreateRequest, ApiKeyCreateResponse, ApiKeyInfo, ApiKeyListResponse
from app.schemas.response import success
from app.services import api_key as api_key_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/apply", response_model=None)
async def apply_api_key(
    req: ApiKeyCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Apply for a new API Key."""
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


@router.get("/keys", response_model=None)
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    _: ApiKey = Depends(require_auth),
):
    """List all API Keys (requires authentication)."""
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


@router.post("/revoke", response_model=None)
async def revoke_api_key(
    app_id: str,
    db: AsyncSession = Depends(get_db),
    _: ApiKey = Depends(require_auth),
):
    """Revoke an API Key (requires authentication)."""
    await api_key_service.revoke_api_key(db, app_id)
    return success(message="API Key has been revoked")
