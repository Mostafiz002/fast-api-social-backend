"""create posts table

Revision ID: 08524b9b37fe
Revises: 
Create Date: 2026-07-18 15:49:09.437768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08524b9b37fe'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
