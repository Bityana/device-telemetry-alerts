from services.api.app.app.security.auth import decode_token
from jose import jwt
from datetime import datetime, timedelta, timezone


def test_decode_token_scopes():
    secret = "test-secret"
    now = datetime.now(timezone.utc)
    payload = {
        "iss": "issuer",
        "aud": "aud",
        "sub": "u1",
        "scopes": ["telemetry:write"],
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=5)).timestamp()),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    p = decode_token(token, secret=secret, issuer="issuer", audience="aud")
    assert p.sub == "u1"
    assert "telemetry:write" in p.scopes
