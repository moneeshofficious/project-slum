# tools/fix_json_no_bom.py
from __future__ import annotations
from pathlib import Path
import json

def rewrite_no_bom(p: Path) -> None:
    s = p.read_text(encoding="utf-8-sig")  # accepts BOM
    # Validate JSON (ensures file isn't just comments/whitespace)
    json.loads(s)
    p.write_text(s, encoding="utf-8")  # writes WITHOUT BOM

def main():
    base = Path("tests/conversations")
    for jf in base.glob("*.json"):
        rewrite_no_bom(jf)
        print("Rewrote without BOM:", jf)

if __name__ == "__main__":
    main()
