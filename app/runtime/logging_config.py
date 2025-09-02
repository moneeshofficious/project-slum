# app/runtime/logging_config.py
from __future__ import annotations
import logging

def configure_logging(level_str: str = "INFO") -> logging.Logger:
    level = getattr(logging, level_str.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger("app")
    logger.debug("Logging configured at %s", level_str.upper())
    return logger
