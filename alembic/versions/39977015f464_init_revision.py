"""init revision

Revision ID: 39977015f464
Revises: 
Create Date: 2023-10-22 16:16:06.903555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '39977015f464'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "groups",
        sa.Column(
            "group_id",
            sa.String,
            primary_key=True,
            index=True,
            unique=True,
        ),
        sa.Column("group_full_name", sa.String),
        keep_existing=False,
    )
    op.create_table(
        "meps",
        sa.Column(
            "mep_id",
            sa.Integer,
            primary_key=True,
            index=True,
            unique=True,
        ),
        sa.Column("full_name", sa.String),
        sa.Column("current_group_id", sa.String),
        sa.Column("country", sa.String),
        sa.Column("is_active", sa.Boolean),
        keep_existing=False,
    )
    op.create_foreign_key(
        "fk_groups_meps",
        "meps",
        "groups",
        ["current_group_id"],
        ["group_id"],
    )
    op.create_table(
        "resolutions",
        sa.Column(
            "resolution_id",
            sa.String,
            primary_key=True,
            index=True,
            unique=True,
        ),
        sa.Column("type", sa.String),
        sa.Column("url", sa.String),
        sa.Column("label", sa.String),
        sa.Column("date", sa.TIMESTAMP),
        sa.Column("page_number", sa.Integer),
        keep_existing=False,
    )
    op.create_table(
        "votes",
        sa.Column(
            "votes_id",
            sa.UUID,
            primary_key=True,
            index=True,
        ),
        sa.Column("mep_id", sa.Integer),
        sa.Column("value", sa.String),
        sa.Column("resolution_id", sa.String),
        sa.Column("group_id_at_vote", sa.String),
        keep_existing=False,
    )
    op.create_foreign_key(
        "fk_meps_votes",
        "votes",
        "meps",
        ["mep_id"],
        ["mep_id"],
    )
    op.create_foreign_key(
        "fk_resolutions_votes",
        "votes",
        "resolutions",
        ["resolution_id"],
        ["resolution_id"],
    )
    op.create_table(
        "mep_events",
        sa.Column(
            "id",
            sa.UUID,
            primary_key=True,
            index=True,
            unique=True
        ),
        sa.Column("mep_id", sa.Integer),
        sa.Column("type", sa.String),
        sa.Column("value", sa.String),
        sa.Column("date", sa.TIMESTAMP),
        keep_existing=False,
    )
    op.create_foreign_key(
        "fk_meps_events",
        "mep_events",
        "meps",
        ["mep_id"],
        ["mep_id"],
    )


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.Inspector.from_engine(conn)
    sql_tables = inspector.get_table_names()
    tables = [
        "mep_events",
        "votes",
        "resolutions",
        "meps",
        "groups",
    ]
    for t in tables:
        if t in sql_tables:
            op.drop_table(t)
