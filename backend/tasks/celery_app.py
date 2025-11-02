"""
Celery設定 - 定期更新ジョブ
"""

from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()

# RedisのURL（デフォルトはローカル）
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "spotify_analytics",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# 1日1回実行（毎日午前3時）
celery_app.conf.beat_schedule = {
    "update-spotify-data-daily": {
        "task": "tasks.tasks.update_spotify_data",
        "schedule": crontab(hour=3, minute=0),
    },
}

celery_app.conf.timezone = "UTC"

