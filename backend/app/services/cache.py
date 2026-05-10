import json
from collections.abc import Callable
from typing import TypeVar

from app.db.redis import get_redis

T = TypeVar("T")


def get_json(key: str) -> dict | None:
    value = get_redis().get(key)
    if value is None:
        return None
    return json.loads(value)


def set_json(key: str, value: dict, ttl_seconds: int = 60) -> None:
    get_redis().setex(key, ttl_seconds, json.dumps(value, default=str))


def invalidate(*keys: str) -> None:
    if keys:
        get_redis().delete(*keys)


def cached_json(key: str, factory: Callable[[], T], ttl_seconds: int = 60) -> T:
    cached = get_json(key)
    if cached is not None:
        return cached  # type: ignore[return-value]
    value = factory()
    if isinstance(value, dict):
        set_json(key, value, ttl_seconds)
    return value

