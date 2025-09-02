# app/feedback.py
"""
Lightweight feedback capture for learning loop.
Usage:
  from app.feedback import record_feedback
  record_feedback(user="tester", category="helpfulness", rating=4, note="Good.")
"""
from __future__ import annotations
import json, pathlib, time
LOG = pathlib.Path("data/feedback")
LOG.mkdir(parents=True, exist_ok=True)
FILE = LOG / "feedback.jsonl"

def record_feedback(user: str, category: str, rating: int, note: str = "") -> None:
    evt = {
        "ts": int(time.time()),
        "user": user,
        "category": category,
        "rating": int(rating),
        "note": note,
    }
    with FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False) + "\n")
