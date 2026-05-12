import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

security = HTTPBearer(auto_error=False)


def _b64encode(payload: bytes) -> str:
    return base64.urlsafe_b64encode(payload).rstrip(b"=").decode("ascii")


def _b64decode(payload: str) -> bytes:
    padding = "=" * (-len(payload) % 4)
    return base64.urlsafe_b64decode(payload + padding)


def _sign(message: str) -> str:
    digest = hmac.new(settings.jwt_secret.encode(), message.encode(), hashlib.sha256).digest()
    return _b64encode(digest)


def create_access_token(username: str, role: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": username,
        "role": role,
        "exp": int((datetime.now(UTC) + timedelta(hours=8)).timestamp()),
    }
    encoded_header = _b64encode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = _b64encode(json.dumps(payload, separators=(",", ":")).encode())
    message = f"{encoded_header}.{encoded_payload}"
    return f"{message}.{_sign(message)}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, signature = token.split(".")
        message = f"{encoded_header}.{encoded_payload}"
        if not hmac.compare_digest(signature, _sign(message)):
            raise ValueError("bad signature")
        payload = json.loads(_b64decode(encoded_payload))
        if int(payload["exp"]) < int(datetime.now(UTC).timestamp()):
            raise ValueError("expired")
        return payload
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сессия недействительна или истекла. Войдите в систему заново.",
        ) from exc


def authenticate_user(username: str, password: str) -> dict[str, str] | None:
    if username == settings.admin_username and hmac.compare_digest(password, settings.admin_password):
        return {"username": username, "role": "admin"}
    if username == settings.operator_username and hmac.compare_digest(password, settings.operator_password):
        return {"username": username, "role": "operator"}
    return None


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict[str, str]:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходимо войти в систему.")
    payload = decode_access_token(credentials.credentials)
    return {"username": str(payload["sub"]), "role": str(payload["role"])}


def require_roles(*roles: str):
    def dependency(user: dict[str, str] = Depends(get_current_user)) -> dict[str, str]:
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения операции.",
            )
        return user

    return dependency

