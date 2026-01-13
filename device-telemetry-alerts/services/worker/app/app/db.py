from __future__ import annotations

from contextlib import contextmanager
import logging
from psycopg2.pool import SimpleConnectionPool

logger = logging.getLogger(__name__)
_pool: SimpleConnectionPool | None = None


def init_pool(dsn: str) -> None:
    global _pool
    if _pool is not None:
        return
    _pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=dsn)


@contextmanager
def get_conn():
    global _pool
    if _pool is None:
        raise RuntimeError("DB pool not initialized. Call init_pool() at startup.")
    conn = _pool.getconn()
    try:
        yield conn
    finally:
        _pool.putconn(conn)
