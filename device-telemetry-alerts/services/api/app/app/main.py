from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Response, Request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.config import get_settings
from app.db import init_pool, healthcheck
from app.redis_client import get_redis
from app.metrics import REQUEST_LATENCY
from app.telemetry.routes import router as telemetry_router
from app.alerts.routes import router as alerts_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Device Telemetry & Alerts API")

app.include_router(telemetry_router)
app.include_router(alerts_router)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    resp = await call_next(request)
    elapsed = time.time() - start
    REQUEST_LATENCY.labels(request.method, request.url.path, str(resp.status_code)).observe(elapsed)
    return resp


@app.on_event("startup")
def on_startup():
    s = get_settings()
    init_pool(s.postgres_dsn)
    # eager redis ping so failures show up early
    r = get_redis(s.redis_url)
    r.ping()


@app.get("/healthz")
def healthz():
    s = get_settings()
    db_ok = healthcheck()
    redis_ok = True
    try:
        get_redis(s.redis_url).ping()
    except Exception:
        redis_ok = False
    status = 200 if db_ok and redis_ok else 503
    return Response(
        content=f"ok={db_ok and redis_ok}",
        status_code=status,
        media_type="text/plain",
    )


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
