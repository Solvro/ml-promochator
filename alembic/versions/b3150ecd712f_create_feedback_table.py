"""create feedback table

Revision ID: b3150ecd712f
Revises: 
Create Date: 2025-01-30 22:29:29.201131

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "b3150ecd712f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("question", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "supervisor_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("faculty", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("is_adequate", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("feedback")
