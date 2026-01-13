from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status
from .auth import decode_token, require_scopes, Principal
from app.config import get_settings


def get_principal(authorization: str | None = Header(default=None)) -> Principal:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    s = get_settings()
    return decode_token(token, secret=s.jwt_secret, issuer=s.jwt_issuer, audience=s.jwt_audience)


def require(*scopes: str):
    def _dep(p: Principal = Depends(get_principal)) -> Principal:
        require_scopes(p, scopes)
        return p
    return _dep
