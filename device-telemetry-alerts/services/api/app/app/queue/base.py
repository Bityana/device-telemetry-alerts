from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class QueueMessage:
    event_id: UUID
    device_id: str


class QueuePublisher(ABC):
    @abstractmethod
    def publish(self, msg: QueueMessage) -> None:
        raise NotImplementedError
