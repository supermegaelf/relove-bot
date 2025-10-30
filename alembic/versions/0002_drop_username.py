from alembic import op
import sqlalchemy as sa

revision = "0002_drop_username"
down_revision = "0001_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("username")


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("username", sa.String(length=255), nullable=True))
        batch_op.create_index("ix_users_username", ["username"], unique=False)

