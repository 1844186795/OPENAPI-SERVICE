"""达人数据响应模型"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderInfo(BaseModel):
    """达人订单信息"""
    order_id: str = Field(description="订单ID")
    product_id: Optional[str] = Field(None, description="商品ID")
    product_name: Optional[str] = Field(None, description="商品名称")
    sku_id: Optional[str] = Field(None, description="SKU ID")
    product_price: Optional[float] = Field(None, description="商品价格")
    payment_amount: Optional[float] = Field(None, description="支付金额")
    currency: Optional[str] = Field(None, description="货币单位")
    quantity: Optional[int] = Field(None, description="下单件数")
    is_full_refund: Optional[str] = Field(None, description="是否全额退款")
    payment_method: Optional[str] = Field(None, description="付款方式")
    order_status: Optional[str] = Field(None, description="订单状态")
    influencer_username: str = Field(description="达人用户名")
    content_type: Optional[str] = Field(None, description="内容形式")
    content_id: Optional[str] = Field(None, description="内容ID")
    commission_model: Optional[str] = Field(None, description="佣金模式")
    standard_commission_rate: Optional[str] = Field(None, description="标准佣金率")
    estimated_commission_amount: Optional[float] = Field(None, description="预估计佣金额")
    estimated_standard_commission: Optional[float] = Field(None, description="预计标准佣金付款")
    actual_commission_amount: Optional[float] = Field(None, description="实际计佣金额")
    actual_commission: Optional[float] = Field(None, description="实际佣金")
    store_ad_commission_rate: Optional[str] = Field(None, description="店铺广告佣金率")
    estimated_store_ad_commission: Optional[float] = Field(None, description="预计店铺广告佣金付款")
    actual_store_ad_commission: Optional[float] = Field(None, description="实际店铺广告佣金付款")
    estimated_joint_bonus: Optional[float] = Field(None, description="预估合资达人奖金")
    actual_joint_bonus: Optional[float] = Field(None, description="实际合资达人奖金")
    created_time: Optional[datetime] = Field(None, description="订单创建时间")
    payment_time: Optional[datetime] = Field(None, description="支付时间")
    delivery_time: Optional[datetime] = Field(None, description="订单送达时间")
    settlement_time: Optional[datetime] = Field(None, description="佣金结算时间")
    platform: Optional[str] = Field(None, description="平台")
    created_at: Optional[datetime] = Field(None, description="导入时间")
