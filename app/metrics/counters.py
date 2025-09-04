# app/metrics/counters.py
from __future__ import annotations

from typing import Any

try:
    from prometheus_client import Counter as _PromCounter
except Exception:
    _PromCounter = None  # prometheus not installed; we'll no-op


class _NoopChild:
    """No-op child for .labels(...).inc(...) chains."""
    def labels(self, *args: Any, **kwargs: Any) -> "_NoopChild":
        return self

    def inc(self, *args: Any, **kwargs: Any) -> None:
        return


# Backwards-compat no-op counter (has .labels().inc())
_NoOpCounter = _NoopChild


def _make_counter():
    """Create a Counter with the expected 'kind' label, or a no-op if unavailable."""
    if _PromCounter is None:
        return _NoOpCounter()
    try:
        # IMPORTANT: include label 'kind' because callers do .labels(kind="email")
        return _PromCounter(
            "redactions_total",
            "Total number of redactions performed by safety/security layers.",
            ["kind"],
        )
    except Exception:
        # Very old prometheus-client or runtime error — fall back safely
        return _NoOpCounter()


class _CounterProxy:
    """
    Proxy that behaves like the inner counter AND is callable.
    - Supports legacy code: redactions_total().labels(...).inc(...)
    - Supports modern code: redactions_total.labels(...).inc(...)
    """
    def __init__(self, inner):
        self._inner = inner

    def __call__(self, *args, **kwargs):
        # Return the actual counter so call-sites with parentheses keep working
        return self._inner

    def __getattr__(self, name: str):
        return getattr(self._inner, name)


# Public export: acts like a Counter and is also callable
redactions_total = _CounterProxy(_make_counter())
