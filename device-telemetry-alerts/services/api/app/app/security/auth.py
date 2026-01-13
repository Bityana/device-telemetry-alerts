from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from fastapi import HTTPException, status
from jose import jwt, JWTError


@dataclass(frozen=True)
class Principal:
    sub: str
    scopes: set[str]


def decode_token(token: str, *, secret: str, issuer: str, audience: str) -> Principal:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"], issuer=issuer, audience=audience)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    sub = payload.get("sub") or "anonymous"
    scopes = set(payload.get("scopes") or [])
    return Principal(sub=sub, scopes=scopes)


def require_scopes(principal: Principal, required: Iterable[str]) -> None:
    missing = [s for s in required if s not in principal.scopes]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required scopes: {', '.join(missing)}",
        )
