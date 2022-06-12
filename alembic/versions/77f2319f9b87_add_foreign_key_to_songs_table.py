"""add foreign key to songs table

Revision ID: 77f2319f9b87
Revises: f5a5f122d94f
Create Date: 2022-06-11 16:25:58.082397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "77f2319f9b87"
down_revision = "f5a5f122d94f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("songs", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "song_users_fk",
        source_table="songs",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("song_users_fk", table_name="songs")
    op.drop_column("songs", "owner_id")
    pass
