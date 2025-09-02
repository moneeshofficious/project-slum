from __future__ import annotations
from typing import Any

def inc(metric: str, labels: dict[str,str] | None = None) -> None:
    pass

def observe(metric: str, value: float, labels: dict[str,str] | None = None) -> None:
    pass
