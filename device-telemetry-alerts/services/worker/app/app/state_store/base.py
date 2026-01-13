from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class DeviceStateStore(ABC):
    @abstractmethod
    def update_last_seen(self, device_id: str, ts: datetime) -> None:
        raise NotImplementedError
