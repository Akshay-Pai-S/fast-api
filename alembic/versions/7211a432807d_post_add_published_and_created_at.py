"""Post add published and created_at

Revision ID: 7211a432807d
Revises: 8d118512f87b
Create Date: 2026-03-07 13:07:55.629418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7211a432807d'
down_revision: Union[str, Sequence[str], None] = '8d118512f87b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean, server_default='TRUE')
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
