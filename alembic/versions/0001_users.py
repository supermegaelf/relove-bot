from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = "0001_users"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("tg_id", sa.BigInteger, nullable=False, unique=True),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, default=datetime.utcnow),
    )
    op.create_index("ix_users_tg_id", "users", ["tg_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_tg_id", table_name="users")
    op.drop_table("users")


