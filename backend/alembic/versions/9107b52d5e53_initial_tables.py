"""initial_tables

Revision ID: 9107b52d5e53
Revises:
Create Date: 2026-10-25 02:19:25.533779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9107b52d5e53'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables: users, memories."""
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(), nullable=True, unique=True, index=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("public_key", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True, default=True),
    )

    op.create_table(
        "memories",
        sa.Column("id", sa.String(), primary_key=True, nullable=False),
        sa.Column("encrypted_data", sa.String(), nullable=False),
        sa.Column("encrypted_category", sa.String(), nullable=True),
        sa.Column("retention", sa.String(), nullable=False, server_default="until_delete"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.String(), sa.ForeignKey("users.id"), nullable=True),
    )


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table("memories")
    op.drop_table("users")
