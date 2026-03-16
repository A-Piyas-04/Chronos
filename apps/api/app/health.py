from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.database import check_database_ready, get_engine

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str]:
    try:
        check_database_ready(get_engine())
    except Exception as exc:
        raise HTTPException(status_code=503, detail="not ready") from exc
    return {"status": "ok"}
