"""Database connectivity — re-exports for health checks and legacy imports."""

from __future__ import annotations

from app.db.session import check_database_ready, get_engine

__all__ = ["check_database_ready", "get_engine"]
