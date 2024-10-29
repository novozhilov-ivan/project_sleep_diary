"""Create tables

Revision ID: eb6dc73824a4
Revises:
Create Date: 2024-10-28 12:47:02.234543

"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "eb6dc73824a4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("oid", sa.Uuid(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата обновления записи",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата создания записи",
        ),
        sa.PrimaryKeyConstraint("username"),
        sa.UniqueConstraint("oid"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "notes",
        sa.Column("bedtime_date", sa.Date(), nullable=False),
        sa.Column("owner_oid", sa.Uuid(), nullable=False),
        sa.Column("went_to_bed", sa.Time(), nullable=False),
        sa.Column("fell_asleep", sa.Time(), nullable=False),
        sa.Column("woke_up", sa.Time(), nullable=False),
        sa.Column("got_up", sa.Time(), nullable=False),
        sa.Column("no_sleep", sa.Time(), nullable=False),
        sa.Column("oid", sa.Uuid(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата обновления записи",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата создания записи",
        ),
        sa.ForeignKeyConstraint(["owner_oid"], ["users.oid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint(
            "bedtime_date",
            "owner_oid",
            name="unique_bedtime_date_for_user",
        ),
        sa.UniqueConstraint("oid"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notes")
    op.drop_table("users")
    # ### end Alembic commands ###