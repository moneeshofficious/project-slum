# app/metrics/counters.py
"""
Central counters (singleton) to avoid duplicate Prometheus registration.
"""
from __future__ import annotations
from typing import Optional
from prometheus_client import Counter

_REDACTIONS_TOTAL: Optional[Counter] = None

def redactions_total() -> Counter:
    """Global redactions counter, created once.
    Labels: kind = 'email' | 'phone' | 'other'
    """
    global _REDACTIONS_TOTAL
    if _REDACTIONS_TOTAL is None:
        _REDACTIONS_TOTAL = Counter(
            "app_redactions_total",
            "PII redactions performed",
            labelnames=("kind",),
        )
    return _REDACTIONS_TOTAL
