# Architecture Notes

## Goals
This project is intentionally small, but it demonstrates patterns that show up in IoT/security-device fleets:
- **Decoupling**: ingest fast; process asynchronously
- **Idempotency**: accept retries without duplicating side effects
- **Observability**: measure p95 latency and throughput
- **Operational clarity**: health checks + runbooks
- **Pluggable infrastructure**: local dev vs cloud backends

## Services

### API (FastAPI)
Responsibilities:
- Validate and accept telemetry (`POST /v1/telemetry`)
- Persist raw events in Postgres (source of truth)
- Publish message to a queue for background processing
- Expose alerts (`GET /v1/alerts`)
- Expose `/metrics` for Prometheus-style scraping

### Worker
Responsibilities:
- Consume queue messages
- Fetch telemetry event from Postgres
- Apply rules and write alerts to Postgres
- Cache device state (last_seen) in Redis
- Retry + dead-letter pattern (demo implementation)

## Queue backends
- Default: **Redis Streams** (easy local dev)
- Optional: **AWS SQS** (adapter included; configure via env vars)
- Optional: **Kafka** (stubbed; swap-in producer/consumer library)

The point is not to claim Redis Streams == Kafka/SQS, but to show the *interface boundary* so the backend can be replaced.

## Data storage
- Postgres:
  - `telemetry_events` (raw source of truth)
  - `alerts` (derived results)
- Redis:
  - request rate limiting buckets
  - cache of device last-seen timestamps

## Reliability patterns (demo)
- **Idempotency**: `event_id` as a primary key (safe retries)
- **At-least-once delivery**: messages can be retried; worker inserts alerts with a uniqueness constraint to avoid duplicates
- **Dead-letter**: after N attempts, message is sent to a dead-letter stream

## Measuring p95 latency
Use `bench/ingest_bench.py` and Prometheus histograms:
- throughput (req/s)
- p95 latency in ms

For portfolio purposes, include:
- your hardware/env
- concurrency level
- duration
- results
