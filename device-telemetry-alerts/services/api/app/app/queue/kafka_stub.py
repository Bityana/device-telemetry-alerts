from __future__ import annotations

from .base import QueuePublisher, QueueMessage


class KafkaStubPublisher(QueuePublisher):
    """A stub showing where a Kafka backend would plug in.

    For a real implementation, you could use confluent-kafka or kafka-python
    and publish QueueMessage to a topic.
    """

    def publish(self, msg: QueueMessage) -> None:
        raise NotImplementedError(
            "Kafka backend is a stub in this demo. Use QUEUE_BACKEND=redis_streams or sqs."
        )
