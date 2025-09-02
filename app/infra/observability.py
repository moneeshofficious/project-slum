# app/infra/observability.py
"""
Tiny dev-only observability helpers:
- Prometheus exporter (start_http_server)
- Structured logging setup
"""

from __future__ import annotations
import logging
import os
from typing import Optional

def configure_logging(level: str = "INFO") -> None:
    """
    Configure JSON-ish console logging without external deps.
    """
    lvl = getattr(logging, level.upper(), logging.INFO)
    root = logging.getLogger()
    if root.handlers:
        for h in root.handlers:
            root.removeHandler(h)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='{"ts":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","msg":"%(message)s"}',
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
    root.setLevel(lvl)


_exporter_started = False

def maybe_start_metrics_exporter(port: Optional[int] = None) -> None:
    """
    Start Prometheus exporter if ENABLE_METRICS=true (dev).
    Uses port from METRICS_PORT or provided fallback (default 9108).
    Safe to call multiple times; idempotent.
    """
    global _exporter_started
    if _exporter_started:
        return

    if os.environ.get("ENABLE_METRICS", "").lower() not in ("1", "true", "yes", "on"):
        return

    p = port or int(os.environ.get("METRICS_PORT", "9108"))
    try:
        from prometheus_client import start_http_server  # type: ignore
        start_http_server(p)
        logging.getLogger(__name__).info(f"Prometheus metrics exporter started on :{p}")
        _exporter_started = True
    except Exception as e:
        logging.getLogger(__name__).warning(f"Metrics exporter not started: {e}")
