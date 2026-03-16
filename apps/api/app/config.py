from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

load_dotenv()


class Settings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    environment: str = Field(default="local", alias="ENVIRONMENT")
    database_url: str = Field(
        default="postgresql+psycopg2://chronos:chronos@localhost:5432/chronos",
        alias="DATABASE_URL",
    )
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")


@lru_cache
def get_settings() -> Settings:
    return Settings.model_validate(
        {
            "ENVIRONMENT": os.getenv("ENVIRONMENT"),
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "SENTRY_DSN": os.getenv("SENTRY_DSN"),
        }
    )
