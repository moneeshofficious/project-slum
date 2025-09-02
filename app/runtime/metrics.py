# app/runtime/metrics.py
from __future__ import annotations
import os
import logging
from typing import Optional

_logger = logging.getLogger("app.metrics")

# Optional until user installs prometheus_client
try:
    from prometheus_client import Counter, Gauge, start_http_server
    _PROM_AVAILABLE = True
except Exception:  # noqa: BLE001
    _PROM_AVAILABLE = False
    Counter = object  # type: ignore
    Gauge = object    # type: ignore
    def start_http_server(*args, **kwargs):  # type: ignore
        raise RuntimeError("prometheus_client not installed")

_boot_counter: Optional["Counter"] = None
_health_gauge: Optional["Gauge"] = None
_started = False

def maybe_start_metrics() -> None:
    """Start the exporter if ENABLE_METRICS=true and prometheus_client is available."""
    global _started, _boot_counter, _health_gauge
    enable = os.getenv("ENABLE_METRICS", "false").lower() == "true"
    port = int(os.getenv("METRICS_PORT", "9108"))
    if not enable:
        _logger.info("Metrics disabled (set ENABLE_METRICS=true to enable).")
        return
    if not _PROM_AVAILABLE:
        _logger.warning(
            "Metrics requested but prometheus_client not installed. "
            "Run: pip install prometheus-client"
        )
        return
    if _started:
        return
    start_http_server(port)  # Exposes metrics at http://localhost:<port>/
    _boot_counter = Counter("app_boot_count", "Number of times the app booted in this process")
    _health_gauge = Gauge("app_health", "1=healthy")
    _health_gauge.set(1)
    _started = True
    _logger.info("Metrics exporter running at http://localhost:%d/", port)

def bump_boot_counter() -> None:
    if _PROM_AVAILABLE and _boot_counter is not None:
        _boot_counter.inc()
