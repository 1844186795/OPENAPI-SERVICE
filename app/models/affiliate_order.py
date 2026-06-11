"""达人订单模型"""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, DECIMAL, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AffiliateOrder(BaseModel):
    """TikTok Shop 达人带货订单表"""
    __tablename__ = "affiliate_orders"
    __table_args__ = {"comment": "达人订单表"}

    # 批次追踪
    upload_batch_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="上传批次标识")
    upload_date: Mapped[date] = mapped_column(Date, server_default=func.current_date(), nullable=False, comment="上传日期")

    # 订单基本信息
    order_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="订单ID")
    product_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="商品ID")
    product_name: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="商品名称")
    sku_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="SKU ID")
    product_price: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="商品价格")
    payment_amount: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="支付金额")
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="货币单位")
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="下单件数")
    is_full_refund: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="是否全额退款（是/否）")
    payment_method: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="付款方式")
    order_status: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="订单状态")

    # 达人信息
    influencer_username: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True, comment="达人用户名")
    content_type: Mapped[str | None] = mapped_column(String(16), nullable=True, comment="内容形式（视频/直播）")
    content_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="内容ID")

    # 佣金信息
    commission_model: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="佣金模式")
    standard_commission_rate: Mapped[str | None] = mapped_column(String(16), nullable=True, comment="标准佣金率")
    estimated_commission_amount: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="预估计佣金额")
    estimated_standard_commission: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="预计标准佣金付款")
    actual_commission_amount: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="实际计佣金额")
    actual_commission: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="实际佣金")
    store_ad_commission_rate: Mapped[str | None] = mapped_column(String(16), nullable=True, comment="店铺广告佣金率")
    estimated_store_ad_commission: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="预计店铺广告佣金付款")
    actual_store_ad_commission: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="实际店铺广告佣金付款")
    estimated_joint_bonus: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="预估合资达人奖金")
    actual_joint_bonus: Mapped[float | None] = mapped_column(DECIMAL(10, 2), nullable=True, comment="实际合资达人奖金")

    # 时间信息
    created_time: Mapped[datetime | None] = mapped_column(DateTime, index=True, nullable=True, comment="订单创建时间")
    payment_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="支付时间")
    delivery_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="订单送达时间")
    settlement_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="佣金结算时间")

    # 平台
    platform: Mapped[str | None] = mapped_column(String(16), nullable=True, comment="平台（如 TTS）")
