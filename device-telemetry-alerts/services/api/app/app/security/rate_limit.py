from __future__ import annotations

import time
import redis
from fastapi import HTTPException, status


def enforce_rate_limit(
    r: redis.Redis,
    *,
    key: str,
    limit: int,
    window_sec: int,
) -> None:
    """Very small Redis-based fixed-window limiter (demo).

    Good enough to show the pattern; production versions typically use sliding windows/leaky bucket.
    """
    now = int(time.time())
    bucket = now // window_sec
    redis_key = f"rl:{key}:{bucket}"

    current = r.incr(redis_key)
    if current == 1:
        r.expire(redis_key, window_sec + 1)

    if current > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )
