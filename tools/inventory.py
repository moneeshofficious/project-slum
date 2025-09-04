# tools/inventory.py
"""
Inventory tool (pruned):
- Writes: docs/inventory.md, docs/inventory.csv, docs/tree.txt
- Creates previews for source/docs only (skips venv/caches)
- Saves: git_status.txt, git_log.txt, pytest_summary.txt, requirements_freeze.txt
Run:
  python tools/inventory.py
"""
from __future__ import annotations
import os, sys, csv, hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PREV = DOCS / "preview"
EXCLUDE_DIRS = {
    ".git", ".venv", ".mypy_cache", "__pycache__", ".pytest_cache", ".ruff_cache",
    ".idea", ".vscode", "node_modules", ".hypothesis"
}
INCLUDE_EXT = {".py", ".md", ".txt", ".json", ".yml", ".yaml", ".ini"}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:12]

def head_lines(p: Path, n: int = 80) -> str:
    try:
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            return "".join([next(f) for _ in range(n)])
    except StopIteration:
        return ""
    except Exception as e:
        return f"[error reading {p.name}: {e}]"

def main() -> int:
    DOCS.mkdir(exist_ok=True)
    PREV.mkdir(parents=True, exist_ok=True)

    files = []

    # Walk with pruning so we never descend into excluded dirs
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Prune
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        # Skip docs/preview (outputs of this tool)
        if Path(dirpath).resolve() == PREV.resolve():
            continue
        for name in filenames:
            p = Path(dirpath) / name
            rel = p.relative_to(ROOT)
            ext = p.suffix.lower()
            sz = p.stat().st_size
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
            lines = 0
            if ext in INCLUDE_EXT:
                try:
                    with p.open("r", encoding="utf-8", errors="ignore") as f:
                        lines = sum(1 for _ in f)
                except Exception:
                    lines = 0
            files.append({
                "path": str(rel),
                "ext": ext or "(none)",
                "bytes": sz,
                "lines": lines,
                "modified": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                "hash12": sha256_file(p),
            })

    files.sort(key=lambda x: (x["path"].lower()))

    # CSV
    csv_path = DOCS / "inventory.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(files[0].keys()) if files else ["path"])
        w.writeheader()
        for row in files:
            w.writerow(row)

    # Tree (ASCII, compact)
    tree_txt = DOCS / "tree.txt"
    with tree_txt.open("w", encoding="utf-8") as f:
        for relpath in [x["path"] for x in files]:
            f.write(relpath + "\n")

    # Markdown summary
    md = DOCS / "inventory.md"
    total_files = len(files)
    total_bytes = sum(x["bytes"] for x in files)
    py_lines = sum(x["lines"] for x in files if x["ext"] == ".py")
    with md.open("w", encoding="utf-8") as f:
        f.write("# Project Inventory\n\n")
        f.write(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- Files counted: {total_files}\n")
        f.write(f"- Total size: {total_bytes} bytes\n")
        f.write(f"- Python LOC (approx): {py_lines}\n\n")
        f.write("## Top 20 biggest files (post-prune)\n\n")
        big = sorted(files, key=lambda x: x["bytes"], reverse=True)[:20]
        for b in big:
            f.write(f"- {b['path']} ({b['bytes']} bytes)\n")
        f.write("\n## Tree tip\nOpen docs/tree.txt for the full list.\n")

    # Previews: only for source/docs files
    for row in files:
        p = ROOT / row["path"]
        if p.suffix.lower() in INCLUDE_EXT and not str(p).startswith(str(PREV)):
            safe = row["path"].replace("\\", "_").replace("/", "_")
            out = PREV / f"{safe}.head.txt"
            with out.open("w", encoding="utf-8") as f:
                f.write(f"===== {row['path']} =====\n{head_lines(p, 80)}")

    # Save git, pytest, and pip info
    os.system(f'git status -sb > "{DOCS / "git_status.txt"}" 2>&1')
    os.system(f'git log --oneline -n 50 > "{DOCS / "git_log.txt"}" 2>&1')
    os.system(f'pytest -q > "{DOCS / "pytest_summary.txt"}" 2>&1')
    py = sys.executable
    os.system(f'"{py}" -m pip freeze > "{DOCS / "requirements_freeze.txt"}" 2>&1')

    print(f"[ok] Wrote: {csv_path}, {md}, {tree_txt}, preview/*.head.txt, git_status, git_log, pytest_summary, requirements_freeze")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
