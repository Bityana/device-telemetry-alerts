from __future__ import annotations

import logging
import time

import redis
from prometheus_client import start_http_server

from app.config import get_settings
from app.db import init_pool
from app.metrics import MESSAGES_CONSUMED, MESSAGES_DEAD_LETTERED
from app.queue.redis_streams import RedisStreamsConsumer
from app.queue.sqs import SQSConsumer
from app.queue.kafka_stub import KafkaStubConsumer
from app.processor import process_message
from app.state_store.redis_store import RedisStateStore
from app.state_store.dynamodb_store import DynamoDBStateStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


def _consumer(r: redis.Redis):
    s = get_settings()
    if s.queue_backend == "redis_streams":
        return RedisStreamsConsumer(
            r,
            stream_name=s.stream_name,
            group=s.consumer_group,
            consumer=s.consumer_name,
        )
    if s.queue_backend == "sqs":
        return SQSConsumer(queue_url=s.sqs_queue_url or "", region=s.aws_region)
    if s.queue_backend == "kafka_stub":
        return KafkaStubConsumer()
    raise ValueError(f"Unknown QUEUE_BACKEND={s.queue_backend}")


def _state_store(r: redis.Redis):
    s = get_settings()
    if s.state_backend == "redis":
        return RedisStateStore(r)
    if s.state_backend == "dynamodb":
        return DynamoDBStateStore(table_name=s.dynamodb_table or "", region=s.aws_region)
    raise ValueError(f"Unknown STATE_BACKEND={s.state_backend}")


def main() -> None:
    s = get_settings()
    init_pool(s.postgres_dsn)

    r = redis.Redis.from_url(s.redis_url, decode_responses=True)
    r.ping()

    # Expose Prometheus metrics on :9000
    start_http_server(9000)

    consumer = _consumer(r)
    state_store = _state_store(r)

    logger.info("Worker started (queue=%s state=%s)", s.queue_backend, s.state_backend)

    while True:
        msgs = consumer.receive(max_messages=10, block_ms=2000)
        if not msgs:
            continue

        for msg in msgs:
            MESSAGES_CONSUMED.inc()
            try:
                process_message(msg, r, state_store)
                consumer.ack(msg.raw_id)
            except Exception as e:
                # Small retry/dead-letter example for Redis Streams; for SQS use DLQ configuration.
                key = f"attempts:{msg.raw_id}"
                attempts = r.incr(key)
                if attempts == 1:
                    r.expire(key, 3600)
                if attempts >= s.max_attempts:
                    consumer.dead_letter(msg, reason=str(e))
                    consumer.ack(msg.raw_id)
                    MESSAGES_DEAD_LETTERED.inc()
                    logger.error("Dead-lettered msg=%s attempts=%s err=%s", msg.raw_id, attempts, e)
                else:
                    logger.warning("Will retry msg=%s attempts=%s err=%s", msg.raw_id, attempts, e)
        time.sleep(0.01)


if __name__ == "__main__":
    main()
