"""Create tasks table

Revision ID: 001
Revises:
Create Date: 2026-01-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create tasks table with UUID primary key."""
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )

    # Create index on completed for filtering queries
    op.create_index('ix_tasks_completed', 'tasks', ['completed'])

    # Create index on created_at for ordering queries
    op.create_index('ix_tasks_created_at', 'tasks', ['created_at'])


def downgrade() -> None:
    """Drop tasks table."""
    op.drop_index('ix_tasks_created_at', table_name='tasks')
    op.drop_index('ix_tasks_completed', table_name='tasks')
    op.drop_table('tasks')
