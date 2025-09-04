# tools/backup_db.py
"""
Backup the local SQLite DB to ./backups/db-YYYYMMDD-HHMMSS.sqlite
Usage:
  python tools/backup_db.py
"""
from __future__ import annotations
import shutil
from pathlib import Path
from datetime import datetime

SRC = Path("app/data/app.db")
DST_DIR = Path("backups")
DST_DIR.mkdir(parents=True, exist_ok=True)

def main() -> None:
    if not SRC.exists():
        print(f"[warn] {SRC} not found; nothing to back up.")
        return
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = DST_DIR / f"db-{ts}.sqlite"
    shutil.copy2(SRC, dst)
    print(f"[ok] Backup written: {dst}")

if __name__ == "__main__":
    main()
