from __future__ import annotations

from prometheus_client import Counter

MESSAGES_CONSUMED = Counter("worker_messages_consumed_total", "Messages consumed by worker")
ALERTS_CREATED = Counter("worker_alerts_created_total", "Alerts created by worker")
MESSAGES_DEAD_LETTERED = Counter("worker_messages_dead_lettered_total", "Messages moved to dead-letter")
