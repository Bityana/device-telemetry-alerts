from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Alert:
    alert_type: str
    severity: str
    message: str


def evaluate_rules(device_id: str, metrics: dict[str, Any]) -> list[Alert]:
    alerts: list[Alert] = []

    temp = metrics.get("temperature_c")
    if isinstance(temp, (int, float)) and temp >= 75:
        alerts.append(Alert("OVERHEAT", "high", f"Device {device_id} temperature {temp}C exceeds threshold"))

    battery = metrics.get("battery_pct")
    if isinstance(battery, (int, float)) and battery <= 15:
        alerts.append(Alert("LOW_BATTERY", "medium", f"Device {device_id} battery {battery}% below threshold"))

    return alerts
