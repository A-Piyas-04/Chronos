from __future__ import annotations

import sentry_sdk
from fastapi import FastAPI

from app.config import get_settings
from app.health import router as health_router

settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn)

app = FastAPI(title="Chronos API")
app.include_router(health_router)
