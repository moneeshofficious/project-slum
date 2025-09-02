# tools/index_refresh.py
"""
Dummy index refresh script to simulate knowledge refresh step.
Run:
  (.venv) PS> python tools/index_refresh.py
"""
from __future__ import annotations
from pathlib import Path
import time, json

OUT = Path("data/index")
OUT.mkdir(parents=True, exist_ok=True)
STAMP = OUT / "last_refresh.json"

def main() -> int:
    STAMP.write_text(json.dumps({"refreshed_at": int(time.time())}), encoding="utf-8")
    print(f"Wrote {STAMP}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
