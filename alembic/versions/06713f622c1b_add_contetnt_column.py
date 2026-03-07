"""Add contetnt column

Revision ID: 06713f622c1b
Revises: 494fc5593d7c
Create Date: 2026-03-07 08:55:16.701378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06713f622c1b'
down_revision: Union[str, Sequence[str], None] = '494fc5593d7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('content', sa.String, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
