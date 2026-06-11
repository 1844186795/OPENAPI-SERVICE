"""达人数据导入与查询 API"""
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.excel.base_validator import FileValidationError
from app.core.excel.daren_parser import DarenOrderParser
from app.core.security.deps import require_auth, require_auth_simple
from app.database import get_db
from app.models.api_key import ApiKey
from app.schemas.daren import OrderInfo
from app.schemas.response import LatestUploadDateResponse, PageResponse, UploadResult, success
from app.services import daren as daren_service

logger = logging.getLogger("openapi-service")

router = APIRouter(prefix="/daren", tags=["达人数据"])


@router.post("/upload", response_model=None, summary="上传导入达人订单",
             description="上传 .xlsx 格式的达人订单文件，解析后批量导入数据库。文件需符合指定格式（30列表头完全一致）。需要携带有效的 API Key 进行身份认证。")
async def upload_orders(
    file: UploadFile = File(..., description="达人订单 Excel 文件（.xlsx）"),
    db: AsyncSession = Depends(get_db),
    _: ApiKey = Depends(require_auth_simple),
):
    """上传达人订单 Excel 文件并导入数据库"""
    # 读取文件内容
    file_content = await file.read()

    # 解析 Excel 文件（含三阶段校验：基本校验 → 格式校验 → 内容校验）
    parser = DarenOrderParser()
    try:
        parse_result = parser.parse(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type,
        )
    except FileValidationError as e:
        return success(
            data=UploadResult(
                batch_id="",
                total_rows=0,
                success_rows=0,
                failed_rows=0,
                failures=[{"row": 0, "reason": e.message}],
            ).model_dump(),
            message=f"文件校验失败：{e.message}",
        )
    except ValueError as e:
        return success(
            data=UploadResult(
                batch_id="",
                total_rows=0,
                success_rows=0,
                failed_rows=0,
                failures=[{"row": 0, "reason": str(e)}],
            ).model_dump(),
            message=f"文件格式错误：{str(e)}",
        )

    # 没有有效数据
    if not parse_result.data:
        return success(
            data=UploadResult(
                batch_id="",
                total_rows=parse_result.total_rows,
                success_rows=0,
                failed_rows=parse_result.failed_rows,
                failures=parse_result.failures,
            ).model_dump(),
            message="文件中没有有效的订单数据",
        )

    # 导入数据库
    batch_id = daren_service.generate_batch_id()
    upload_date = datetime.now(timezone.utc).date()
    success_count, import_failures = await daren_service.batch_import_orders(
        db=db,
        data=parse_result.data,
        batch_id=batch_id,
        upload_date=upload_date,
    )

    result = UploadResult(
        batch_id=batch_id,
        total_rows=parse_result.total_rows,
        success_rows=success_count,
        failed_rows=parse_result.total_rows - success_count,
        failures=parse_result.failures + [
            {"row": f["row"], "reason": f["reason"]}
            for f in import_failures
        ],
    )

    if result.failed_rows == 0:
        return success(data=result.model_dump(), message=f"导入成功，共 {result.success_rows} 条记录")
    else:
        return success(
            data=result.model_dump(),
            message=f"导入完成（成功 {result.success_rows} 条，失败 {result.failed_rows} 条）",
        )


@router.get("/orders", response_model=None, summary="查询达人订单列表",
            description="分页查询已导入的达人订单数据，支持按达人用户名和订单状态筛选。需要携带有效的 API Key 进行身份认证。")
async def list_orders(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    influencer_username: str = Query(None, description="达人用户名（筛选）"),
    order_status: str = Query(None, description="订单状态（筛选）"),
    db: AsyncSession = Depends(get_db),
    _: ApiKey = Depends(require_auth),
):
    """查询达人订单列表"""
    items, total = await daren_service.get_order_list(
        db=db,
        page=page,
        page_size=page_size,
        influencer_username=influencer_username or None,
        order_status=order_status or None,
    )

    return success(
        data=PageResponse[OrderInfo](
            total=total,
            page=page,
            page_size=page_size,
            items=[
                OrderInfo(
                    order_id=item.order_id,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    sku_id=item.sku_id,
                    product_price=float(item.product_price) if item.product_price else None,
                    payment_amount=float(item.payment_amount) if item.payment_amount else None,
                    currency=item.currency,
                    quantity=item.quantity,
                    is_full_refund=item.is_full_refund,
                    payment_method=item.payment_method,
                    order_status=item.order_status,
                    influencer_username=item.influencer_username,
                    content_type=item.content_type,
                    content_id=item.content_id,
                    commission_model=item.commission_model,
                    standard_commission_rate=item.standard_commission_rate,
                    estimated_commission_amount=float(item.estimated_commission_amount) if item.estimated_commission_amount else None,
                    estimated_standard_commission=float(item.estimated_standard_commission) if item.estimated_standard_commission else None,
                    actual_commission_amount=float(item.actual_commission_amount) if item.actual_commission_amount else None,
                    actual_commission=float(item.actual_commission) if item.actual_commission else None,
                    store_ad_commission_rate=item.store_ad_commission_rate,
                    estimated_store_ad_commission=float(item.estimated_store_ad_commission) if item.estimated_store_ad_commission else None,
                    actual_store_ad_commission=float(item.actual_store_ad_commission) if item.actual_store_ad_commission else None,
                    estimated_joint_bonus=float(item.estimated_joint_bonus) if item.estimated_joint_bonus else None,
                    actual_joint_bonus=float(item.actual_joint_bonus) if item.actual_joint_bonus else None,
                    created_time=item.created_time,
                    payment_time=item.payment_time,
                    delivery_time=item.delivery_time,
                    settlement_time=item.settlement_time,
                    platform=item.platform,
                    created_at=item.created_at,
                    upload_date=str(item.upload_date) if item.upload_date else None,
                )
                for item in items
            ],
        ).model_dump()
    )


@router.get("/latest-upload-date", response_model=None, summary="查询最大上传日期",
            description="查询已导入的达人订单数据中最大的上传日期，用于了解数据同步进度。需要携带有效的 API Key 进行身份认证。")
async def latest_upload_date(
    db: AsyncSession = Depends(get_db),
    _: ApiKey = Depends(require_auth),
):
    """查询最大上传日期"""
    max_date = await daren_service.get_latest_upload_date(db)
    return success(
        data=LatestUploadDateResponse(
            latest_upload_date=str(max_date) if max_date else None,
        ).model_dump()
    )
