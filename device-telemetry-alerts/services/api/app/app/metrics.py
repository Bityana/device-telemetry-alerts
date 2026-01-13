from __future__ import annotations

import time
from prometheus_client import Counter, Histogram

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency",
    labelnames=("method", "path", "status"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5),
)

TELEMETRY_INGESTED = Counter(
    "telemetry_ingested_total",
    "Telemetry events ingested",
)

QUEUE_PUBLISHED = Counter(
    "telemetry_queue_published_total",
    "Telemetry messages published to queue",
)
