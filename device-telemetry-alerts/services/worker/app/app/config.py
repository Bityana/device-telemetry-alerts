from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    postgres_dsn: str
    redis_url: str
    queue_backend: str
    stream_name: str
    consumer_group: str
    consumer_name: str

    # Optional AWS
    aws_region: str | None
    sqs_queue_url: str | None

    # Optional state store
    state_backend: str
    dynamodb_table: str | None

    # Processing
    max_attempts: int


def get_settings() -> Settings:
    return Settings(
        postgres_dsn=os.environ.get("POSTGRES_DSN", "postgresql://telemetry:telemetry@localhost:5432/telemetry"),
        redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        queue_backend=os.environ.get("QUEUE_BACKEND", "redis_streams"),
        stream_name=os.environ.get("STREAM_NAME", "telemetry-events"),
        consumer_group=os.environ.get("CONSUMER_GROUP", "telemetry-workers"),
        consumer_name=os.environ.get("CONSUMER_NAME", os.environ.get("HOSTNAME", "worker")),
        aws_region=os.environ.get("AWS_REGION") or None,
        sqs_queue_url=os.environ.get("SQS_QUEUE_URL") or None,
        state_backend=os.environ.get("STATE_BACKEND", "redis"),
        dynamodb_table=os.environ.get("DYNAMODB_TABLE") or None,
        max_attempts=int(os.environ.get("MAX_ATTEMPTS", "5")),
    )
