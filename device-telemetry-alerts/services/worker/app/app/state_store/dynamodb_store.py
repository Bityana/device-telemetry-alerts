from __future__ import annotations

from datetime import datetime, timezone
import boto3

from .base import DeviceStateStore


class DynamoDBStateStore(DeviceStateStore):
    """Optional AWS DynamoDB state store (demo adapter).

    Use when you want device state in a durable, horizontally scalable KV store.
    """

    def __init__(self, table_name: str, region: str | None = None) -> None:
        if not table_name:
            raise ValueError("DYNAMODB_TABLE must be set when STATE_BACKEND=dynamodb")
        self.table_name = table_name
        self.ddb = boto3.resource("dynamodb", region_name=region)
        self.table = self.ddb.Table(table_name)

    def update_last_seen(self, device_id: str, ts: datetime) -> None:
        epoch = int(ts.replace(tzinfo=timezone.utc).timestamp())
        self.table.put_item(Item={"device_id": device_id, "last_seen": epoch})
