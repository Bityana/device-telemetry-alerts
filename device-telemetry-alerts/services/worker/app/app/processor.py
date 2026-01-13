from __future__ import annotations

import logging
from uuid import UUID

import redis

from app.db import get_conn
from app.queue.base import QueueMessage
from app.rules import evaluate_rules
from app.state_store.base import DeviceStateStore
from app.metrics import ALERTS_CREATED

logger = logging.getLogger(__name__)


def _fetch_event(event_id: UUID):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT device_id, event_ts, metrics
                FROM telemetry_events
                WHERE event_id = %s;
                """,
                (str(event_id),),
            )
            row = cur.fetchone()
    return row


def _insert_alert(device_id: str, alert_type: str, severity: str, message: str, event_id: UUID | None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO alerts (device_id, alert_type, severity, message, event_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (device_id, alert_type, event_id) DO NOTHING;
                """,
                (device_id, alert_type, severity, message, str(event_id) if event_id else None),
            )
        conn.commit()


def process_message(msg: QueueMessage, r: redis.Redis, state_store: DeviceStateStore) -> None:
    row = _fetch_event(msg.event_id)
    if not row:
        raise RuntimeError(f"Missing telemetry event {msg.event_id}")

    device_id, event_ts, metrics = row[0], row[1], row[2]

    # Update device state (Redis or DynamoDB) - small demo of pluggable state storage
    state_store.update_last_seen(device_id, event_ts)

    alerts = evaluate_rules(device_id, metrics)
    for a in alerts:
        _insert_alert(device_id, a.alert_type, a.severity, a.message, msg.event_id)
        ALERTS_CREATED.inc()
