from __future__ import annotations

import logging

from worker.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="worker.example_task")
def example_task() -> str:
    logger.info("Chronos worker example_task executed")
    return "ok"
