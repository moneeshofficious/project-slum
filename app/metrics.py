# app/metrics.py
from __future__ import annotations
import logging, os

log = logging.getLogger("app.metrics")

def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        log.debug("%s not set; default=%s", name, default)
        return default
    val = raw.strip().lower() in {"1", "true", "on", "yes"}
    log.debug("Parsed %s=%r -> %s", name, raw, val)
    return val

def start_metrics_if_enabled() -> None:
    if not _env_flag("ENABLE_METRICS", default=False):
        log.info("Metrics disabled (set ENABLE_METRICS=true to enable).")
        return
    port = int(os.getenv("METRICS_PORT", "9108"))
    # start_http_server(port)  # your existing start call
    log.info("Metrics exporter running at http://localhost:%s/", port)
