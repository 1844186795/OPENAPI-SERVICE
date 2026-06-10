"""达人数据业务逻辑层"""
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.affiliate_order import AffiliateOrder


def generate_batch_id() -> str:
    """生成上传批次ID"""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = uuid.uuid4().hex[:8]
    return f"batch_{today}_{suffix}"


async def batch_import_orders(
    db: AsyncSession,
    data: list[dict],
    batch_id: str,
) -> tuple[int, list[dict]]:
    """批量导入达人订单数据

    Args:
        db: 数据库会话
        data: 解析后的订单数据列表（含 _excel_row 行号）
        batch_id: 上传批次标识

    Returns:
        (成功数, 失败详情列表)
    """
    success_count = 0
    failures = []

    for item in data:
        row_num = item.pop("_excel_row", "-")
        try:
            # 检查 order_id 是否已存在
            result = await db.execute(
                select(AffiliateOrder).where(AffiliateOrder.order_id == item["order_id"])
            )
            existing = result.scalar_one_or_none()
            if existing:
                failures.append({"row": row_num, "reason": f"订单ID {item['order_id']} 已存在"})
                continue

            # 构造模型实例（日期已在解析器中转为 ISO 格式字符串）
            order = AffiliateOrder(
                upload_batch_id=batch_id,
                **{k: v for k, v in item.items() if k not in ("created_time", "payment_time", "delivery_time", "settlement_time")},
            )
            # 处理时间字段（ISO 字符串转 datetime）
            for time_field in ["created_time", "payment_time", "delivery_time", "settlement_time"]:
                dt_val = item.get(time_field)
                if dt_val:
                    setattr(order, time_field, datetime.fromisoformat(dt_val))

            db.add(order)
            await db.flush()
            success_count += 1

        except Exception as e:
            failures.append({"row": row_num, "reason": str(e)})

    return success_count, failures


async def get_order_list(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    influencer_username: Optional[str] = None,
    order_status: Optional[str] = None,
) -> tuple[list[AffiliateOrder], int]:
    """查询达人订单列表

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页条数
        influencer_username: 达人用户名筛选
        order_status: 订单状态筛选

    Returns:
        (订单列表, 总条数)
    """
    query = select(AffiliateOrder)

    if influencer_username:
        query = query.where(AffiliateOrder.influencer_username == influencer_username)
    if order_status:
        query = query.where(AffiliateOrder.order_status == order_status)

    # 总条数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页
    query = query.order_by(AffiliateOrder.created_time.desc().nullslast())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    items = list(result.scalars().all())

    return items, total
