from __future__ import annotations

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.core.exceptions import ChronosError
from app.health import router as health_router

settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn)

app = FastAPI(title="Chronos API")


@app.exception_handler(ChronosError)
async def chronos_error_handler(_request: Request, exc: ChronosError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "code": exc.code},
    )


app.include_router(health_router)
