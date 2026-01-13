from __future__ import annotations

from uuid import uuid4
from fastapi import APIRouter, Depends
from psycopg2.extras import Json

from app.config import get_settings
from app.db import get_conn
from app.redis_client import get_redis
from app.metrics import TELEMETRY_INGESTED, QUEUE_PUBLISHED
from app.queue.base import QueueMessage
from app.queue.redis_streams import RedisStreamsPublisher
from app.queue.sqs import SQSPublisher
from app.queue.kafka_stub import KafkaStubPublisher
from app.security.dependencies import require, Principal
from app.security.rate_limit import enforce_rate_limit
from app.security.audit import audit
from .schemas import TelemetryIn, TelemetryAccepted

router = APIRouter(tags=["telemetry"])


def _publisher():
    s = get_settings()
    r = get_redis(s.redis_url)
    if s.queue_backend == "redis_streams":
        return RedisStreamsPublisher(r)
    if s.queue_backend == "sqs":
        return SQSPublisher(queue_url=s.sqs_queue_url or "", region=s.aws_region)
    if s.queue_backend == "kafka_stub":
        return KafkaStubPublisher()
    raise ValueError(f"Unknown QUEUE_BACKEND={s.queue_backend}")


@router.post("/v1/telemetry", response_model=TelemetryAccepted, status_code=202)
def ingest_telemetry(
    payload: TelemetryIn,
    p: Principal = Depends(require("telemetry:write")),
):
    s = get_settings()
    r = get_redis(s.redis_url)

    # Basic per-principal rate limit (demo)
    enforce_rate_limit(r, key=p.sub, limit=240, window_sec=60)

    audit("telemetry.ingest", p, device_id=payload.device_id)

    event_id = payload.event_id or uuid4()

    inserted = False
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO telemetry_events (event_id, device_id, event_ts, metrics)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (event_id) DO NOTHING;
                """,
                (str(event_id), payload.device_id, payload.timestamp, Json(payload.metrics)),
            )
            inserted = cur.rowcount == 1
        conn.commit()

    # Only publish to queue if we wrote a new event
    if inserted:
        TELEMETRY_INGESTED.inc()
        pub = _publisher()
        pub.publish(QueueMessage(event_id=event_id, device_id=payload.device_id))
        QUEUE_PUBLISHED.inc()

    return TelemetryAccepted(event_id=event_id)
