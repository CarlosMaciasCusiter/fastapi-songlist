"""create songs table

Revision ID: 9ffa7d9a1c50
Revises: 
Create Date: 2022-06-11 15:38:32.080304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9ffa7d9a1c50"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "songs",
        sa.Column("id", sa.INTEGER(), nullable=False, primary_key=True),
        sa.Column("tite", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("songs")
