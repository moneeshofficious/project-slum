# tools/detect_architecture.py
"""
Checks for required SLUM architecture files and prints what's missing.
Run:
  python tools/detect_architecture.py
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "app/web/main.py",
    "app/orchestrator/core.py",
    "app/state/machine.py",
    "app/personalization/style.py",
    "app/safety/safety.py",
    "app/security/security.py",
    "app/observability/logging.py",
    "app/data/database.py",
    "app/data/models.py",
    "alembic.ini",
    "app/data/migrations/env.py",
    "app/data/migrations/versions/0001_initial.py",
    "tests/test_smoke.py",
]

def main() -> int:
    missing = []
    present = []
    for rel in REQUIRED:
        p = ROOT / rel
        (present if p.exists() else missing).append(rel)
    print("=== SLUM Architecture Check ===")
    print("\nPresent:")
    for x in present:
        print("  ✓", x)
    print("\nMissing:")
    for x in missing:
        print("  ✗", x)

    # Bonus: short app/ tree for quick visual
    print("\n=== app/ tree (first 200 entries) ===")
    count = 0
    for path in sorted((ROOT / "app").rglob("*")):
        rel = path.relative_to(ROOT)
        print(" ", rel)
        count += 1
        if count >= 200:
            print("  … (truncated)")
            break

    # Write a focused tree for review
    out = ROOT / "docs" / "project_tree_app.txt"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for path in sorted((ROOT / "app").rglob("*")):
            f.write(str(path.relative_to(ROOT)) + "\n")
    print(f"\n[ok] Wrote: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
