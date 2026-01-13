from __future__ import annotations

from uuid import UUID
import json
import redis

from .base import QueuePublisher, QueueMessage


class RedisStreamsPublisher(QueuePublisher):
    def __init__(self, r: redis.Redis, stream_name: str = "telemetry-events") -> None:
        self.r = r
        self.stream_name = stream_name

    def publish(self, msg: QueueMessage) -> None:
        self.r.xadd(
            self.stream_name,
            {"event_id": str(msg.event_id), "device_id": msg.device_id},
            maxlen=200000,
            approximate=True,
        )
