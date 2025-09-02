# app/__main__.py
"""
Entry point for `python -m app`.
Boots logging, starts metrics if enabled, and keeps the process running.
"""
from __future__ import annotations
import os
import time
import logging
from app.runtime.bootstrap import init_runtime

def main() -> None:
    logger = init_runtime()
    logger.info("App boot complete. Press Ctrl+C to exit.")
    # Keep the process alive so the metrics endpoint stays up.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down…")

if __name__ == "__main__":
    main()
