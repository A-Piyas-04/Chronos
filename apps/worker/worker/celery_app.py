from __future__ import annotations

import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

celery_app = Celery("chronos_worker", broker=broker_url)
celery_app.autodiscover_tasks(["worker.tasks"])
