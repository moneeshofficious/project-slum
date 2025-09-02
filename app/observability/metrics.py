# app/observability/metrics.py
from __future__ import annotations
from collections import defaultdict
from typing import Dict

_COUNTERS: Dict[str, int] = defaultdict(int)

def inc(name: str, by: int = 1) -> None:
    _COUNTERS[name] += by

def get(name: str) -> int:
    return _COUNTERS.get(name, 0)

def snapshot() -> Dict[str, int]:
    return dict(_COUNTERS)

def reset() -> None:
    _COUNTERS.clear()

# Named counters for Module 1
RISK_TRIGGERS = "risk_triggers_count"
SCOPE_BLOCKS = "scope_blocks_count"
DEI_REWRITES = "dei_rewrites_count"
CONSENT_ACCEPT = "consent_accept_count"
