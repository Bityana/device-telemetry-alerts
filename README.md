# Device Telemetry & Alerts Platform (Microservices)

A small but production-minded **distributed-systems demo** inspired by real-world IoT / security-device fleets:

- **Ingest API (FastAPI)** accepts device telemetry over REST
- **Queue-based async processing** (default: Redis Streams; optional adapters for **AWS SQS** and **Kafka**)
- **Worker service** evaluates alert rules and writes alerts to **Postgres**
- **Redis** used for caching device state + rate limiting
- **Web console** (**React + TypeScript + SCSS Modules**) to triage alerts
- **Mobile companion app** (**React Native (Expo + TypeScript)**) to view alerts on the go
- **Docker Compose** for 1-command local demo
- **Kubernetes manifests** + **Terraform (toy AWS)** examples for deploy scaffolding
- **Security-minded**: JWT auth + scoped RBAC, input validation, rate limiting, audit logging, CI checks

> This repo is designed for GitHub/portfolio use: clear docs, runnable locally, and easy to extend.

## Architecture (high level)

```
Devices -> FastAPI /v1/telemetry
                |
                v
          Queue (Redis Streams)
                |
                v
        Worker evaluates rules
                |
                v
          Postgres (alerts)
                |
                v
     React Admin Console (alerts)
```

## Quick start (local)

### 1) Requirements
- Docker + Docker Compose
- (Optional) Python 3.11+ for running tests/bench locally

### 2) Run it
```bash
cp .env.example .env
docker compose up --build
```

### 3) Create a dev token (JWT)
In another terminal:
```bash
docker compose exec api python -m app.scripts.generate_token --scopes telemetry:write alerts:read
```

### 4) Send telemetry
```bash
TOKEN="<paste token>"
curl -X POST "http://localhost:8000/v1/telemetry" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "cam-001",
    "timestamp": "2026-01-12T12:00:00Z",
    "metrics": {"temperature_c": 82, "battery_pct": 12}
  }'
```

### 5) View alerts
- API: `GET http://localhost:8000/v1/alerts`
- Web console: `http://localhost:5173`

### 6) Run the mobile app (React Native)
```bash
cd mobile
npm install
npm run start
```

Tip: For a physical phone, set the API Base URL in-app to your machine's LAN IP (e.g., `http://192.168.1.10:8000`).

## Benchmarks (generate your own numbers)
Run the included load test harness and capture **throughput** + **p95 latency**:

```bash
python bench/ingest_bench.py --url http://localhost:8000 --seconds 15 --concurrency 50
```

The script prints rps and latency percentiles. Put those numbers in your resume/GitHub README.

## Deploy scaffolding
- `infra/k8s/` includes basic Kubernetes manifests (api/worker + Postgres/Redis)
- `infra/terraform/aws/` includes a small Terraform starter that provisions:
  - SQS queue (optional)
  - DynamoDB table (optional state store)
  - IAM policy examples

## Notes on “SQS/Kafka/DynamoDB”
This repo runs locally with **Redis Streams + Postgres + Redis** by default. To keep the demo easy to run:
- **SQS** and **DynamoDB** adapters are included but optional (toggle via env vars)
- A **Kafka adapter stub** is included to show how the queue backend would be swapped

See `docs/ARCHITECTURE.md` for details.

## License
MIT (see LICENSE).
