from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class QueueMessage:
    event_id: UUID
    device_id: str
    raw_id: str  # message id (stream id / receipt handle)


class QueueConsumer(ABC):
    @abstractmethod
    def receive(self, *, max_messages: int = 10, block_ms: int = 2000) -> list[QueueMessage]:
        raise NotImplementedError

    @abstractmethod
    def ack(self, raw_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def dead_letter(self, msg: QueueMessage, reason: str) -> None:
        raise NotImplementedError
