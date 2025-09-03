# app/observability/logging.py
"""
Tiny logging bridge. If you already have logging config, we just call it.
Falls back to Python logging.basicConfig.
"""
from __future__ import annotations
import logging

def configure_logging(level: str = "INFO") -> None:
    try:
        # Prefer your existing runtime or observability config if available
        from app.runtime.logging_config import setup_logging as setup1  # type: ignore
        setup1(level)
        return
    except Exception:
        pass
    try:
        from app.observability.logging_cfg import setup_logging as setup2  # type: ignore
        setup2(level)
        return
    except Exception:
        pass
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))

logger = logging.getLogger("slum")
