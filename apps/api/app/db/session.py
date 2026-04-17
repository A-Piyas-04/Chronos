"""Database engine and session factory."""

from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        future=True,
    )


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(
        bind=get_engine(),
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=Session,
        future=True,
    )


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: one session per request; services own commits."""
    factory = get_session_factory()
    db = factory()
    try:
        yield db
    finally:
        db.close()


def check_database_ready(engine: Engine) -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
