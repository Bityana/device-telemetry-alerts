from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.db import get_conn
from app.security.dependencies import require, Principal
from app.security.audit import audit
from .schemas import AlertOut

router = APIRouter(tags=["alerts"])


@router.get("/v1/alerts", response_model=list[AlertOut])
def list_alerts(
    limit: int = Query(default=50, ge=1, le=500),
    p: Principal = Depends(require("alerts:read")),
):
    audit("alerts.list", p, limit=limit)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT alert_id, device_id, alert_type, severity, message, created_at
                FROM alerts
                ORDER BY created_at DESC
                LIMIT %s;
                """,
                (limit,),
            )
            rows = cur.fetchall()

    return [
        AlertOut(
            alert_id=row[0],
            device_id=row[1],
            alert_type=row[2],
            severity=row[3],
            message=row[4],
            created_at=row[5],
        )
        for row in rows
    ]
