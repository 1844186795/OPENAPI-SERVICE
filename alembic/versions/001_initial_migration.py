"""Initial migration: create api_keys table

Revision ID: 001
Revises:
Create Date: 2026-06-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "api_keys",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.String(length=32), nullable=False, comment="Public application ID"),
        sa.Column("app_name", sa.String(length=100), nullable=False, comment="Application name"),
        sa.Column("client_secret", sa.Text(), nullable=False, comment="Client secret for HMAC signing"),
        sa.Column(
            "status",
            sa.Enum("active", "disabled", "expired", name="api_key_status"),
            nullable=False,
            server_default="active",
            comment="Key status",
        ),
        sa.Column("expires_at", sa.DateTime(), nullable=True, comment="Expiration time"),
        sa.Column("description", sa.String(length=255), nullable=True, comment="Description"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_api_keys_app_id"), "api_keys", ["app_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_api_keys_app_id"), table_name="api_keys")
    op.drop_table("api_keys")
