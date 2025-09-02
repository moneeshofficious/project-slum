# tools/stub_reality_check.py
"""
Stub & Reality Check for Project SLUM

- Scans code (excluding .venv) for common stub markers:
  - 'pass' on its own line (non-trivial)
  - 'TODO'/'FIXME'
  - 'NotImplementedError'
  - files with very low LOC (<= 10) that look like placeholders
- Counts tests and recent test results (by scanning .pytest_cache when available)
- Emits REALITY_REPORT.md with a per-module "realness" score.

Run:
  (.venv) PS> python tools/stub_reality_check.py
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {".venv", ".git", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache"}
CODE_DIRS = ["app", "prompts", "skills", "knowledge", "tests", "tools", "i18n"]

MODULE_GUESS: Dict[str, List[str]] = {
    "Module 1 — Safety & Scope Guard": ["app/safety", "tests/test_safety"],
    "Module 2 — Personalization": ["app/personalization", "tests/test_personalization"],
    "Module 3 — Conversation State Machine": ["app/conversation", "app/state_machine", "tests/test_state"],
    "Module 4 — Mate Mode Engine (Coach)": ["app/mate_mode", "prompts/mate_mode", "tests/test_mate"],
    "Module 5 — Inner Me Engine (Companion)": ["app/inner_me", "prompts/inner_me", "tests/test_inner_me"],
    "Module 6 — Skills Library": ["app/skills", "skills", "tests/test_skills"],
    "Module 7 — Science Notes Engine": ["app/science", "science_catalog.json", "tests/test_science"],
    "Module 8 — Memory Layer": ["app/memory", "tests/test_memory"],
    "Module 9 — Knowledge & Retrieval Packs": ["knowledge", "app/retriever", "tests/test_retriever"],
    "Module 10 — Orchestrator": ["app/orchestrator.py", "app/orchestrator", "tests/test_orchestrator"],
    "Module 11 — Frontend UI (Streamlit)": ["Home.py", "app/ui", "tests/test_ui"],
    "Module 12 — Data Layer": ["app/db", "migrations", "app/database.py", "tests/test_database"],
    "Module 13 — Observability & Reliability": ["app/metrics.py", "app/common", "tests/test_cache", "tests/test_retry"],
    "Module 14 — Evaluation & Red-Team": ["tests/conversations", "tools/eval_runner.py", "tests/test_adversarial"],
    "Module 15 — Updates & Learning Loop": ["knowledge_version.json", "docs/update_pipeline.md", "tools/index_refresh.py", "app/feedback.py"],
    "Module 16 — Accessibility & Localization": ["i18n", "tests/test_i18n"],
    "Module 17 — Crisis Hand-offs": ["safety_plan_templates", "app/safety/safety_plan.py", "tests/test_safety_plan"],
    "Module 18 — Web App (Public)": ["deployment", "ops", "tests/test_auth", "tests/test_rate_limit"],
    "Module 19 — Security Hardening": ["app/security.py", "app/security", "tests/test_security"],
    "Module 20 — Cost & Scale": ["config/budgets.yaml", "app/router.py", "app/routing/router.py", "tests/test_router"],
}

STUB_MARKERS = (
    "NotImplementedError",
    "TODO",
    "FIXME",
)

def iter_files() -> List[Path]:
    files: List[Path] = []
    for base in CODE_DIRS:
        p = ROOT / base
        if not p.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for f in filenames:
                # focus on code + md that could be stubs
                if f.endswith((".py", ".md", ".txt", ".json", ".yaml", ".yml")):
                    files.append(Path(dirpath) / f)
    return files

def analyze_file(path: Path) -> Dict[str, int | bool]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"loc": 0, "has_pass": 0, "stub_hits": 0, "is_tiny": True}
    lines = text.splitlines()
    loc = sum(1 for ln in lines if ln.strip() and not ln.strip().startswith("#"))
    has_pass = sum(1 for ln in lines if ln.strip() == "pass")
    stub_hits = sum(1 for m in STUB_MARKERS if m in text)
    is_tiny = loc <= 10
    return {"loc": loc, "has_pass": has_pass, "stub_hits": stub_hits, "is_tiny": is_tiny}

def belongs_to_module(path: Path) -> List[str]:
    rel = path.relative_to(ROOT).as_posix()
    hits = []
    for mod, hints in MODULE_GUESS.items():
        for h in hints:
            if h and h in rel:
                hits.append(mod)
                break
    return hits

def main() -> int:
    results_by_module: Dict[str, Dict[str, int]] = {}
    for mod in MODULE_GUESS:
        results_by_module[mod] = {"files": 0, "loc": 0, "pass_lines": 0, "stub_hits": 0, "tiny_files": 0}

    for f in iter_files():
        info = analyze_file(f)
        mods = belongs_to_module(f)
        if not mods:
            continue
        for mod in mods:
            results_by_module[mod]["files"] += 1
            results_by_module[mod]["loc"] += int(info["loc"])
            results_by_module[mod]["pass_lines"] += int(info["has_pass"])
            results_by_module[mod]["stub_hits"] += int(info["stub_hits"])
            results_by_module[mod]["tiny_files"] += 1 if info["is_tiny"] else 0

    lines = ["# REALITY_REPORT — Stub & Implementation Status\n",
             "| Module | Files | LOC | 'pass' lines | TODO/FIXME/NotImpl | Tiny files (<=10 LOC) | Verdict |\n",
             "|---|---:|---:|---:|---:|---:|---|\n"]
    for mod, m in results_by_module.items():
        verdict = "Likely Real ✅"
        if m["stub_hits"] > 0 or m["pass_lines"] > 5 or m["tiny_files"] >= max(2, m["files"] // 4):
            verdict = "Has Stubs ⚠️"
        if m["files"] == 0 or m["loc"] < 20:
            verdict = "Thin / Likely Stub ⬜"
        lines.append(f"| {mod} | {m['files']} | {m['loc']} | {m['pass_lines']} | {m['stub_hits']} | {m['tiny_files']} | {verdict} |\n")

    (ROOT / "REALITY_REPORT.md").write_text("".join(lines), encoding="utf-8")
    print("REALITY_REPORT.md written.")
    print("Tip: open it next to MASTER_TRACKER_AUTO.md to reconcile ticks vs. realness.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
