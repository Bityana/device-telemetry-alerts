from __future__ import annotations

import json
from uuid import UUID
import boto3

from .base import QueueConsumer, QueueMessage


class SQSConsumer(QueueConsumer):
    def __init__(self, queue_url: str, region: str | None = None) -> None:
        if not queue_url:
            raise ValueError("SQS_QUEUE_URL must be set when QUEUE_BACKEND=sqs")
        self.queue_url = queue_url
        self.client = boto3.client("sqs", region_name=region)

    def receive(self, *, max_messages: int = 10, block_ms: int = 2000) -> list[QueueMessage]:
        resp = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=min(max_messages, 10),
            WaitTimeSeconds=max(0, block_ms // 1000),
        )
        out: list[QueueMessage] = []
        for m in resp.get("Messages", []):
            body = json.loads(m["Body"])
            out.append(
                QueueMessage(
                    event_id=UUID(body["event_id"]),
                    device_id=body["device_id"],
                    raw_id=m["ReceiptHandle"],
                )
            )
        return out

    def ack(self, raw_id: str) -> None:
        self.client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=raw_id)

    def dead_letter(self, msg: QueueMessage, reason: str) -> None:
        # In real SQS you'd configure a DLQ; here we just log.
        print(f"[DLQ] {msg.raw_id} reason={reason}")
