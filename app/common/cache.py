from __future__ import annotations
_cache: dict[str, tuple[str, float]] = {}

def cache_get(key: str) -> str | None:
    return _cache.get(key, (None,0.0))[0]

def cache_put(key: str, value: str, ttl: float = 60.0) -> None:
    _cache[key] = (value, ttl)
