# app/runtime/bootstrap.py
from __future__ import annotations
import logging
import os
from app.runtime.logging_config import configure_logging
from app.runtime.metrics import maybe_start_metrics, bump_boot_counter

def init_runtime() -> logging.Logger:
    logger = configure_logging(os.getenv("LOG_LEVEL", "INFO"))
    logger.debug("Initializing runtime…")
    # Start metrics (no-op if disabled or prometheus_client missing)
    maybe_start_metrics()
    bump_boot_counter()
    return logger
