# app/metrics/__init__.py
from __future__ import annotations
import logging
import os

from .counters import redactions_total

log = logging.getLogger("app.metrics")


def _env_flag(name: str, default: bool = False) -> bool:
    """Parse truthy env vars: 1/true/on/yes (case-insensitive)."""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "on", "yes"}


def maybe_start_metrics_exporter() -> None:
    """Start Prometheus exporter if ENABLE_METRICS is set truthy."""
    if not _env_flag("ENABLE_METRICS", False):
        log.info("Metrics disabled (set ENABLE_METRICS=true to enable).")
        return
    try:
        from prometheus_client import start_http_server  # lazy import
    except Exception as e:
        log.warning("Prometheus not available: %s", e)
        return
    port = int(os.getenv("METRICS_PORT", "9108"))
    start_http_server(port)
    log.info("Metrics exporter running at http://localhost:%s/", port)
