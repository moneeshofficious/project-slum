# app/main.py
from app.orchestrator.pipeline import run_inference
from app.observability.logging_cfg import get_logger
from __future__ import annotations
import os
from app.tools.guard_harness import main
log = get_logger(__name__)

def quick_demo():
    reply = run_inference(
        mode="inner_me",
        user_message="I'm feeling a bit overwhelmed today.",
        session_id="demo",
        user_profile={"age_band": "adult", "pronouns": "they/them", "tone": "warm", "pacing": "normal", "culture_notes": "IN"},
    )
    print("\n--- DEMO OUTPUT ---\n")
    print(reply)

if __name__ == "__main__":
    log.info("Starting quick demo…")
    quick_demo()
    os.environ.setdefault("ENABLE_METRICS", "true")
    os.environ.setdefault("METRICS_PORT", "9108")
    os.environ.setdefault("LOG_LEVEL", "INFO")
    main()