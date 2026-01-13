from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.config import get_settings


def main() -> None:
    s = get_settings()
    ap = argparse.ArgumentParser(description="Generate a dev JWT for local testing.")
    ap.add_argument("--sub", default="dev-user", help="Subject/user id")
    ap.add_argument("--scopes", nargs="+", default=["telemetry:write", "alerts:read"], help="Scopes")
    ap.add_argument("--minutes", type=int, default=120, help="Token lifetime (minutes)")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    payload = {
        "iss": s.jwt_issuer,
        "aud": s.jwt_audience,
        "sub": args.sub,
        "scopes": args.scopes,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=args.minutes)).timestamp()),
    }
    token = jwt.encode(payload, s.jwt_secret, algorithm="HS256")
    print(token)


if __name__ == "__main__":
    main()
