"""add user table

Revision ID: c292d1592d25
Revises: 8e9a40b255c4
Create Date: 2026-07-18 19:55:23.489575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c292d1592d25'
down_revision: Union[str, Sequence[str], None] = '8e9a40b255c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False),       
        sa.Column('password', sa.String(), nullable=False),       
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),       
        sa.PrimaryKeyConstraint('id'),       
        sa.UniqueConstraint('email'),       
        )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
