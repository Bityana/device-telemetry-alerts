from __future__ import annotations

import redis


def get_redis(redis_url: str) -> redis.Redis:
    # decode_responses=True => strings in/out
    return redis.Redis.from_url(redis_url, decode_responses=True)
