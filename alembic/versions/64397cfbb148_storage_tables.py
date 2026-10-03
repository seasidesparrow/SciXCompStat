"""Add matching data tables
Revision ID: 64397cfbb148
Revises: 250da2879efe
Create Date: 2026-09-05 20:04:00
"""
import sqlalchemy as sa
from alembic import op
from dateutil import tz
from datetime import datetime

import compstat.models as models

# revision identifiers, used by Alembic.
revision = "64397cfbb148"
down_revision = "250da2879efe"
branch_labels = None
depends_on = None

def get_now():
    timestamp = datetime.utcnow().replace(tzinfo=tz.tzutc())
    return timestamp


def upgrade():
    # storage for Crossref Set IDs for harvesting
    op.create_table(
        "setidents",
        sa.Column("setidentid", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("bibstem", sa.String(), nullable=True),
        sa.Column("issn", sa.JSON(), nullable=True),
        sa.Column("journal", sa.String(), nullable=True),
        sa.Column("crossrefid", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False, default=get_now()),
        sa.Column("updated", sa.DateTime(), nullable=False, onupdate=get_now()),
        sa.PrimaryKeyConstraint("uniqid"),
        sa.UniqueConstraint("uniqid"),
    )

    # master record for each doi
    op.create_table(
        "master",
        sa.Column("masterid", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("input_file", sa.String(), nullable=False),
        sa.Column("doi", sa.String(), nullable=False),
        sa.Column("journalid", sa.JSON(), nullable=True),
        sa.Column("origin", sa.String(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("bibcode", sa.String(), nullable=True),
        sa.Column("scix_id", sa.String(), nullable=True),
        sa.Column("is_valid", sa.Boolean(), default=False, nullable=False),
        sa.Column("doi_found", sa.Boolean(), default=False, nullable=False),
        sa.Column("meta_found", sa.Boolean(), default=False, nullable=False)
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True, default=get_now()),
        sa.Column("updated", sa.DateTime(), nullable=True, onupdate=get_now()),
        sa.PrimaryKeyConstraint("masterid"),
        sa.UniqueConstraint("doi"),
        sa.UniqueConstraint("masterid"),
    )

    # summary record for each bibstem, per volume
    op.create_table(
        "summary",
        sa.Column("summaryid", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("journalid", sa.String(), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.Column("volume_letter", sa.String(), nullable=True),
        sa.Column("paper_count", sa.Integer(), nullable=False),
        sa.Column("complete_fraction", sa.Float(), nullable=True),
        sa.Column("complete_by_year", sa.Text(), nullable=True),
        sa.Column("complete_details", sa.Text(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True, default=get_now()),
        sa.Column("updated", sa.DateTime(), nullable=True, onupdate=get_now()),
        sa.PrimaryKeyConstraint("summaryid"),
        sa.UniqueConstraint("summaryid"),
    )

    # harvest log, one row per setid per harvest
    op.create_table(
        "harvestlog",
        sa.Column("harvestid", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("crossrefid", sa.String(), nullable=False),
        sa.Column("recordcount", sa.Integer(), nullable=False),
        sa.Column("lastharvest", sa.DateTime(), nullable=False, default="2026-01-01Z00:00:00"),
        sa.Column("currentharvest", sa.DateTime(), nullable=False, onupdate=get_now()),
        sa.PrimaryKeyConstraing("harvestid"),
        sa.UniqueConstraint("harvestid"),
    )

    # ### end Alembic upgrade commands ###


def downgrade():

    op.drop_table("harvestlog")
    op.drop_table("summary")
    op.drop_table("master")
    op.drop_table("setidents")

    # ### end Alembic downgrade commands ###
