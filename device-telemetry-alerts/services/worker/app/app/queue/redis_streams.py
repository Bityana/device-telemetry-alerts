from __future__ import annotations

from uuid import UUID
import redis

from .base import QueueConsumer, QueueMessage


class RedisStreamsConsumer(QueueConsumer):
    def __init__(
        self,
        r: redis.Redis,
        *,
        stream_name: str,
        group: str,
        consumer: str,
        dead_letter_stream: str = "telemetry-dead-letter",
    ) -> None:
        self.r = r
        self.stream_name = stream_name
        self.group = group
        self.consumer = consumer
        self.dead_letter_stream = dead_letter_stream

        # Create group if missing
        try:
            self.r.xgroup_create(self.stream_name, self.group, id="0", mkstream=True)
        except redis.exceptions.ResponseError as e:
            # BUSYGROUP means it already exists
            if "BUSYGROUP" not in str(e):
                raise

    def receive(self, *, max_messages: int = 10, block_ms: int = 2000) -> list[QueueMessage]:
        resp = self.r.xreadgroup(
            groupname=self.group,
            consumername=self.consumer,
            streams={self.stream_name: ">"},
            count=max_messages,
            block=block_ms,
        )
        out: list[QueueMessage] = []
        for _stream, messages in resp:
            for msg_id, fields in messages:
                try:
                    event_id = UUID(fields["event_id"])
                    device_id = fields["device_id"]
                    out.append(QueueMessage(event_id=event_id, device_id=device_id, raw_id=msg_id))
                except Exception:
                    # Malformed; dead-letter
                    out.append(QueueMessage(event_id=UUID(int=0), device_id="unknown", raw_id=msg_id))
        return out

    def ack(self, raw_id: str) -> None:
        self.r.xack(self.stream_name, self.group, raw_id)

    def dead_letter(self, msg: QueueMessage, reason: str) -> None:
        self.r.xadd(self.dead_letter_stream, {"raw_id": msg.raw_id, "reason": reason})
