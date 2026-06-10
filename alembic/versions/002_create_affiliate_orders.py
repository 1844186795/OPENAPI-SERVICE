"""Create affiliate_orders table for daren order data

Revision ID: 002
Revises: 001
Create Date: 2026-06-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "affiliate_orders",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("upload_batch_id", sa.String(length=64), nullable=False, comment="上传批次标识"),
        sa.Column("order_id", sa.String(length=64), nullable=False, comment="订单ID"),
        sa.Column("product_id", sa.String(length=64), nullable=True, comment="商品ID"),
        sa.Column("product_name", sa.String(length=512), nullable=True, comment="商品名称"),
        sa.Column("sku_id", sa.String(length=64), nullable=True, comment="SKU ID"),
        sa.Column("product_price", sa.DECIMAL(10, 2), nullable=True, comment="商品价格"),
        sa.Column("payment_amount", sa.DECIMAL(10, 2), nullable=True, comment="支付金额"),
        sa.Column("currency", sa.String(length=10), nullable=True, comment="货币单位"),
        sa.Column("quantity", sa.Integer(), nullable=True, comment="下单件数"),
        sa.Column("is_full_refund", sa.String(length=10), nullable=True, comment="是否全额退款"),
        sa.Column("payment_method", sa.String(length=32), nullable=True, comment="付款方式"),
        sa.Column("order_status", sa.String(length=32), nullable=True, comment="订单状态"),
        sa.Column("influencer_username", sa.String(length=128), nullable=False, comment="达人用户名"),
        sa.Column("content_type", sa.String(length=16), nullable=True, comment="内容形式"),
        sa.Column("content_id", sa.String(length=64), nullable=True, comment="内容ID"),
        sa.Column("commission_model", sa.String(length=32), nullable=True, comment="佣金模式"),
        sa.Column("standard_commission_rate", sa.String(length=16), nullable=True, comment="标准佣金率"),
        sa.Column("estimated_commission_amount", sa.DECIMAL(10, 2), nullable=True, comment="预估计佣金额"),
        sa.Column("estimated_standard_commission", sa.DECIMAL(10, 2), nullable=True, comment="预计标准佣金付款"),
        sa.Column("actual_commission_amount", sa.DECIMAL(10, 2), nullable=True, comment="实际计佣金额"),
        sa.Column("actual_commission", sa.DECIMAL(10, 2), nullable=True, comment="实际佣金"),
        sa.Column("store_ad_commission_rate", sa.String(length=16), nullable=True, comment="店铺广告佣金率"),
        sa.Column("estimated_store_ad_commission", sa.DECIMAL(10, 2), nullable=True, comment="预计店铺广告佣金付款"),
        sa.Column("actual_store_ad_commission", sa.DECIMAL(10, 2), nullable=True, comment="实际店铺广告佣金付款"),
        sa.Column("estimated_joint_bonus", sa.DECIMAL(10, 2), nullable=True, comment="预估合资达人奖金"),
        sa.Column("actual_joint_bonus", sa.DECIMAL(10, 2), nullable=True, comment="实际合资达人奖金"),
        sa.Column("created_time", sa.DateTime(), nullable=True, comment="订单创建时间"),
        sa.Column("payment_time", sa.DateTime(), nullable=True, comment="支付时间"),
        sa.Column("delivery_time", sa.DateTime(), nullable=True, comment="订单送达时间"),
        sa.Column("settlement_time", sa.DateTime(), nullable=True, comment="佣金结算时间"),
        sa.Column("platform", sa.String(length=16), nullable=True, comment="平台"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id", name="uq_affiliate_orders_order_id"),
        mysql_comment="达人订单表",
    )
    op.create_index(op.f("ix_affiliate_orders_order_id"), "affiliate_orders", ["order_id"])
    op.create_index(op.f("ix_affiliate_orders_influencer_username"), "affiliate_orders", ["influencer_username"])


def downgrade() -> None:
    op.drop_index(op.f("ix_affiliate_orders_influencer_username"), table_name="affiliate_orders")
    op.drop_index(op.f("ix_affiliate_orders_order_id"), table_name="affiliate_orders")
    op.drop_table("affiliate_orders")
