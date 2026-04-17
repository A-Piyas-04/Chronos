"""phase1_initial_schema

Revision ID: d454057b4cc9
Revises:
Create Date: 2026-04-17 23:45:32.117338

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d454057b4cc9"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE TYPE calendar_provider AS ENUM ('google')")
    op.execute("CREATE TYPE task_priority AS ENUM ('low', 'medium', 'high')")
    op.execute("CREATE TYPE task_type AS ENUM ('deep', 'mechanical')")
    op.execute("CREATE TYPE task_status AS ENUM ('inbox', 'scheduled', 'done')")
    op.execute("CREATE TYPE session_source AS ENUM ('system_generated', 'user_manual')")
    op.execute("CREATE TYPE session_status AS ENUM ('scheduled', 'completed', 'missed', 'cancelled')")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("image_url", sa.String(length=2048), nullable=True),
        sa.Column("google_sub", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(
        "ix_users_google_sub",
        "users",
        ["google_sub"],
        unique=False,
        postgresql_where=sa.text("google_sub IS NOT NULL"),
    )

    op.create_table(
        "user_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("workday_start_time", sa.Time(), nullable=False),
        sa.Column("workday_end_time", sa.Time(), nullable=False),
        sa.Column("deep_work_start_time", sa.Time(), nullable=False),
        sa.Column("deep_work_end_time", sa.Time(), nullable=False),
        sa.Column(
            "max_deep_work_block_minutes",
            sa.Integer(),
            server_default="45",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "calendar_accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "provider",
            postgresql.ENUM("google", name="calendar_provider", create_type=False),
            nullable=False,
        ),
        sa.Column("provider_account_id", sa.String(length=512), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("token_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "provider",
            "provider_account_id",
            name="uq_calendar_accounts_user_provider_account",
        ),
    )
    op.create_index(op.f("ix_calendar_accounts_user_id"), "calendar_accounts", ["user_id"], unique=False)

    op.create_table(
        "calendar_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("calendar_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("external_event_id", sa.String(length=1024), nullable=False),
        sa.Column("source_calendar_id", sa.String(length=512), nullable=True),
        sa.Column("title", sa.Text(), server_default="", nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_all_day", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("is_busy", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("raw_status", sa.String(length=64), nullable=True),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["calendar_account_id"], ["calendar_accounts.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "external_event_id",
            name="uq_calendar_events_user_external_event",
        ),
    )
    op.create_index(op.f("ix_calendar_events_user_id"), "calendar_events", ["user_id"], unique=False)
    op.create_index(
        op.f("ix_calendar_events_calendar_account_id"),
        "calendar_events",
        ["calendar_account_id"],
        unique=False,
    )
    op.create_index(
        "ix_calendar_events_user_start",
        "calendar_events",
        ["user_id", "start_at"],
        unique=False,
    )

    op.create_table(
        "tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("estimated_duration_minutes", sa.Integer(), nullable=False),
        sa.Column("remaining_duration_minutes", sa.Integer(), nullable=False),
        sa.Column("deadline_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "priority",
            postgresql.ENUM("low", "medium", "high", name="task_priority", create_type=False),
            nullable=False,
        ),
        sa.Column(
            "task_type",
            postgresql.ENUM("deep", "mechanical", name="task_type", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "status",
            postgresql.ENUM("inbox", "scheduled", "done", name="task_status", create_type=False),
            server_default=sa.text("'inbox'::task_status"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasks_user_id"), "tasks", ["user_id"], unique=False)
    op.create_index("ix_tasks_user_status", "tasks", ["user_id", "status"], unique=False)

    op.create_table(
        "scheduled_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title_snapshot", sa.String(length=512), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "source",
            postgresql.ENUM(
                "system_generated",
                "user_manual",
                name="session_source",
                create_type=False,
            ),
            server_default=sa.text("'system_generated'::session_source"),
            nullable=False,
        ),
        sa.Column(
            "status",
            postgresql.ENUM(
                "scheduled",
                "completed",
                "missed",
                "cancelled",
                name="session_status",
                create_type=False,
            ),
            server_default=sa.text("'scheduled'::session_status"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scheduled_sessions_user_id"), "scheduled_sessions", ["user_id"], unique=False)
    op.create_index(op.f("ix_scheduled_sessions_task_id"), "scheduled_sessions", ["task_id"], unique=False)
    op.create_index(
        "ix_scheduled_sessions_user_start",
        "scheduled_sessions",
        ["user_id", "start_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_scheduled_sessions_user_start", table_name="scheduled_sessions")
    op.drop_index(op.f("ix_scheduled_sessions_task_id"), table_name="scheduled_sessions")
    op.drop_index(op.f("ix_scheduled_sessions_user_id"), table_name="scheduled_sessions")
    op.drop_table("scheduled_sessions")

    op.drop_index("ix_tasks_user_status", table_name="tasks")
    op.drop_index(op.f("ix_tasks_user_id"), table_name="tasks")
    op.drop_table("tasks")

    op.drop_index("ix_calendar_events_user_start", table_name="calendar_events")
    op.drop_index(op.f("ix_calendar_events_calendar_account_id"), table_name="calendar_events")
    op.drop_index(op.f("ix_calendar_events_user_id"), table_name="calendar_events")
    op.drop_table("calendar_events")

    op.drop_index(op.f("ix_calendar_accounts_user_id"), table_name="calendar_accounts")
    op.drop_table("calendar_accounts")

    op.drop_table("user_preferences")

    op.drop_index("ix_users_google_sub", table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    op.execute("DROP TYPE session_status")
    op.execute("DROP TYPE session_source")
    op.execute("DROP TYPE task_status")
    op.execute("DROP TYPE task_type")
    op.execute("DROP TYPE task_priority")
    op.execute("DROP TYPE calendar_provider")
