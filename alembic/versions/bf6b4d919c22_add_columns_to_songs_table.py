"""add columns to songs table

Revision ID: bf6b4d919c22
Revises: 77f2319f9b87
Create Date: 2022-06-11 16:30:29.238404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bf6b4d919c22"
down_revision = "77f2319f9b87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "songs",
        sa.Column("single", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "songs",
        sa.Column(
            "released_on",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("songs", "single")
    op.drop_column("songs", "released_on")
    pass
