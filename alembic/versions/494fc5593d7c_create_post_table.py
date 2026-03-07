"""create post table

Revision ID: 494fc5593d7c
Revises: 
Create Date: 2026-03-05 18:59:53.189224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '494fc5593d7c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
