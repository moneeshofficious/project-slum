# app/observability/audit.py
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
AUDIT_FILE = LOG_DIR / "audit.jsonl"

def write(event_type: str, **fields):
    rec = {"ts": datetime.utcnow().isoformat() + "Z", "type": event_type, **fields}
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
