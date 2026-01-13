from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TelemetryIn(BaseModel):
    event_id: UUID | None = Field(default=None, description="Optional idempotency key")
    device_id: str = Field(min_length=3, max_length=128)
    timestamp: datetime
    metrics: dict[str, Any]


class TelemetryAccepted(BaseModel):
    event_id: UUID
    accepted: bool = True
