from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    postgres_dsn: str
    redis_url: str

    jwt_secret: str
    jwt_issuer: str
    jwt_audience: str

    queue_backend: str
    sqs_queue_url: str | None
    aws_region: str | None


def get_settings() -> Settings:
    return Settings(
        postgres_dsn=os.environ.get("POSTGRES_DSN", "postgresql://telemetry:telemetry@localhost:5432/telemetry"),
        redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        jwt_secret=os.environ.get("JWT_SECRET", "dev-secret-change-me"),
        jwt_issuer=os.environ.get("JWT_ISSUER", "device-telemetry-alerts"),
        jwt_audience=os.environ.get("JWT_AUDIENCE", "device-telemetry-alerts"),
        queue_backend=os.environ.get("QUEUE_BACKEND", "redis_streams"),
        sqs_queue_url=os.environ.get("SQS_QUEUE_URL") or None,
        aws_region=os.environ.get("AWS_REGION") or None,
    )
