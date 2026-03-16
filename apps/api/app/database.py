from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.config import get_settings


def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(settings.database_url, pool_pre_ping=True)


def check_database_ready(engine: Engine) -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
