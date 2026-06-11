"""add_created_time_index

Revision ID: e39f40df9c0a
Revises: 003
Create Date: 2026-06-11 14:35:44.719974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e39f40df9c0a'
down_revision: Union[str, Sequence[str], None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(op.f('ix_affiliate_orders_created_time'), 'affiliate_orders', ['created_time'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_affiliate_orders_created_time'), table_name='affiliate_orders')
