from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AlertOut(BaseModel):
    alert_id: UUID
    device_id: str
    alert_type: str
    severity: str
    message: str
    created_at: datetime
