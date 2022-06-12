"""add artist column to songs table edit name of title column

Revision ID: 4ad870054160
Revises: 9ffa7d9a1c50
Create Date: 2022-06-11 16:11:52.094188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4ad870054160"
down_revision = "9ffa7d9a1c50"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("songs", sa.Column("artist", sa.String(), nullable=False))
    op.alter_column("songs", "tite", nullable=False, new_column_name="title")
    pass


def downgrade() -> None:
    op.drop_column("songs", "artist")
    op.alter_column("songs", "title", nullable=False, new_column_name="tite")
    pass
