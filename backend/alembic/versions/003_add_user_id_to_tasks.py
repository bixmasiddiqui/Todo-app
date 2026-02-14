"""Add user_id to tasks table

Revision ID: 003
Revises: 002
Create Date: 2026-02-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add user_id column to tasks table."""
    op.add_column('tasks', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_foreign_key('fk_tasks_user_id', 'tasks', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Remove user_id column from tasks table."""
    op.drop_constraint('fk_tasks_user_id', 'tasks', type_='foreignkey')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_column('tasks', 'user_id')
