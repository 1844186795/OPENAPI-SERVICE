"""Alter affiliate_orders: drop order_id unique, add upload_date

Revision ID: 003
Revises: 002
Create Date: 2026-06-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 删除 order_id 唯一约束（保留普通索引）
    op.drop_constraint("uq_affiliate_orders_order_id", "affiliate_orders", type_="unique")

    # 2. 新增 upload_date 列，默认当日日期
    op.add_column(
        "affiliate_orders",
        sa.Column(
            "upload_date",
            sa.Date(),
            server_default=sa.text("(CURRENT_DATE)"),
            nullable=False,
            comment="上传日期",
        ),
    )


def downgrade() -> None:
    # 1. 删除 upload_date 列
    op.drop_column("affiliate_orders", "upload_date")

    # 2. 恢复 order_id 唯一约束
    op.create_unique_constraint("uq_affiliate_orders_order_id", "affiliate_orders", ["order_id"])
