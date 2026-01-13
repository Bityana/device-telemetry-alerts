from __future__ import annotations

from datetime import datetime, timezone
import redis


class DeviceStateCache:
    """Redis-backed cache for lightweight device state (demo)."""

    def __init__(self, r: redis.Redis) -> None:
        self.r = r

    def update_last_seen(self, device_id: str, ts: datetime) -> None:
        key = f"device:last_seen:{device_id}"
        self.r.set(key, int(ts.replace(tzinfo=timezone.utc).timestamp()), ex=24 * 3600)

    def get_last_seen(self, device_id: str) -> int | None:
        key = f"device:last_seen:{device_id}"
        v = self.r.get(key)
        return int(v) if v else None
