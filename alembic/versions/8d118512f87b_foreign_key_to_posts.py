"""Foreign key to posts

Revision ID: 8d118512f87b
Revises: 3fd294f82d63
Create Date: 2026-03-07 12:50:32.610571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d118512f87b'
down_revision: Union[str, Sequence[str], None] = '3fd294f82d63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer, nullable=False)
    )
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
