from __future__ import annotations

import argparse
import asyncio
import os
import random
import statistics
import time
from datetime import datetime, timezone
from uuid import uuid4

try:
    import httpx
except Exception:
    raise SystemExit(
        "Missing dependency: httpx. Install with: pip install httpx\n"
        "Or install dev deps: pip install -r requirements-dev.txt"
    )


def pct(values: list[float], p: float) -> float:
    if not values:
        return float("nan")
    values_sorted = sorted(values)
    k = int(round((p / 100.0) * (len(values_sorted) - 1)))
    return values_sorted[k]


async def worker(client: httpx.AsyncClient, url: str, token: str, stop_at: float, latencies: list[float], ok: list[int]):
    while time.time() < stop_at:
        payload = {
            "event_id": str(uuid4()),
            "device_id": f"cam-{random.randint(1, 50):03d}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": {
                "temperature_c": random.choice([30, 45, 55, 65, 78, 82]),
                "battery_pct": random.choice([10, 12, 18, 35, 55, 90]),
            },
        }
        t0 = time.perf_counter()
        try:
            resp = await client.post(
                f"{url}/v1/telemetry",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0,
            )
            dt = (time.perf_counter() - t0) * 1000.0
            latencies.append(dt)
            ok.append(1 if resp.status_code < 300 else 0)
        except Exception:
            dt = (time.perf_counter() - t0) * 1000.0
            latencies.append(dt)
            ok.append(0)


async def main_async(url: str, seconds: int, concurrency: int, token: str):
    latencies: list[float] = []
    ok: list[int] = []

    stop_at = time.time() + seconds
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(worker(client, url, token, stop_at, latencies, ok)) for _ in range(concurrency)]
        await asyncio.gather(*tasks)

    total = len(latencies)
    success = sum(ok)
    rps = total / seconds if seconds > 0 else 0.0

    print("")
    print("=== Ingest benchmark results ===")
    print(f"Total requests: {total}")
    print(f"Success (2xx):  {success} ({(success/total*100.0 if total else 0):.1f}%)")
    print(f"Throughput:    {rps:.1f} req/s")
    print(f"Latency p50:   {pct(latencies, 50):.1f} ms")
    print(f"Latency p95:   {pct(latencies, 95):.1f} ms")
    print(f"Latency p99:   {pct(latencies, 99):.1f} ms")
    print(f"Max latency:   {max(latencies) if latencies else float('nan'):.1f} ms")
    print("")


def main():
    ap = argparse.ArgumentParser(description="Async benchmark for /v1/telemetry")
    ap.add_argument("--url", default="http://localhost:8000", help="API base URL")
    ap.add_argument("--seconds", type=int, default=15, help="Test duration")
    ap.add_argument("--concurrency", type=int, default=50, help="Concurrent workers")
    ap.add_argument("--token", default=os.environ.get("JWT_TOKEN", ""), help="JWT token (telemetry:write)")
    args = ap.parse_args()

    if not args.token:
        raise SystemExit("Missing --token or JWT_TOKEN env var. Generate one with generate_token.py")

    asyncio.run(main_async(args.url.rstrip("/"), args.seconds, args.concurrency, args.token))


if __name__ == "__main__":
    main()
