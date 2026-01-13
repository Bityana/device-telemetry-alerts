# Benchmarks

This folder contains a small harness to measure:
- **Throughput (req/s)**
- **Latency percentiles (p50/p95/p99)**

## Run
1) Start services:
```bash
docker compose up --build
```

2) Generate a token:
```bash
TOKEN=$(docker compose exec -T api python -m app.scripts.generate_token --scopes telemetry:write alerts:read)
```

3) Run the benchmark:
```bash
python bench/ingest_bench.py --token "$TOKEN" --seconds 15 --concurrency 50
```

Copy the numbers into your resume/README.
