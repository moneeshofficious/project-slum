# app/data/migrations/versions/0001_initial.py
from __future__ import annotations
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Keep it minimal & additive (only audit_log). Your existing SQL migrations remain untouched.
    if not op.get_bind().dialect.has_table(op.get_bind(), "audit_log"):  # type: ignore[attr-defined]
        op.create_table(
            "audit_log",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("event", sa.String(64), nullable=False),
            sa.Column("details", sa.Text, nullable=False),
            sa.Column("created_at", sa.DateTime, nullable=False),
        )

def downgrade():
    op.drop_table("audit_log")
