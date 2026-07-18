"""add content column into post

Revision ID: 8e9a40b255c4
Revises: 08524b9b37fe
Create Date: 2026-07-18 19:48:46.288018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e9a40b255c4'
down_revision: Union[str, Sequence[str], None] = '08524b9b37fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
