from __future__ import annotations

import json
from uuid import UUID
import boto3

from .base import QueuePublisher, QueueMessage


class SQSPublisher(QueuePublisher):
    def __init__(self, queue_url: str, region: str | None = None) -> None:
        if not queue_url:
            raise ValueError("SQS_QUEUE_URL must be set when QUEUE_BACKEND=sqs")
        self.queue_url = queue_url
        self.client = boto3.client("sqs", region_name=region)

    def publish(self, msg: QueueMessage) -> None:
        body = json.dumps({"event_id": str(msg.event_id), "device_id": msg.device_id})
        self.client.send_message(QueueUrl=self.queue_url, MessageBody=body)
