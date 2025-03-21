"""Add a feedback column

Revision ID: 74c9a5ac6c6a
Revises: b3150ecd712f
Create Date: 2025-03-21 21:21:18.885577

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '74c9a5ac6c6a'
down_revision: Union[str, None] = 'b3150ecd712f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('prompt_content', sa.String(length=2000), nullable=False),
        sa.Column('prompt_faculty', sa.String(), nullable=True),
        sa.Column('is_adequate', sa.Boolean(), nullable=False),
        sa.Column('papers', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('supervisor_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['supervisor_id'], ['supervisor.id']),
    )


def downgrade() -> None:
    op.drop_table('feedback')
