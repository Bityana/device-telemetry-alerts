from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from .auth import Principal

logger = logging.getLogger("audit")


def audit(action: str, principal: Principal, **fields: Any) -> None:
    """Emit a small structured audit log.

    In production you'd typically send this to a centralized log pipeline.
    """
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "sub": principal.sub,
        "scopes": sorted(list(principal.scopes)),
        **fields,
    }
    # JSON so it's easy to parse/search
    logger.info(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))
