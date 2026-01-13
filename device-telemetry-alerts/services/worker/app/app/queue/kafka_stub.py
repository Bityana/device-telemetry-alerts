from __future__ import annotations

from .base import QueueConsumer, QueueMessage


class KafkaStubConsumer(QueueConsumer):
    def receive(self, *, max_messages: int = 10, block_ms: int = 2000) -> list[QueueMessage]:
        raise NotImplementedError("Kafka backend is a stub in this demo.")

    def ack(self, raw_id: str) -> None:
        raise NotImplementedError("Kafka backend is a stub in this demo.")

    def dead_letter(self, msg: QueueMessage, reason: str) -> None:
        raise NotImplementedError("Kafka backend is a stub in this demo.")
