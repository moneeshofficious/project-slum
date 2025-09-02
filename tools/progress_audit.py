# tools/progress_audit.py
"""
Progress Auditor for Project SLUM

- Scans the project tree (excluding .venv)
- Looks for simple indicators for each module (folders/files/tests)
- Writes MASTER_TRACKER_AUTO.md with a completion % per module
- Prints a short console summary

Run:
  (.venv) PS> python tools/progress_audit.py
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]  # project root (one level up from tools/)
EXCLUDE_DIRS = {".venv", ".git", ".pytest_cache", "__pycache__", ".mypy_cache"}

# Simple presence indicators per module (adjust freely as you add code)
# Note: '**' must be a whole path segment (e.g., '**/*.md'), not '**.md'
MODULE_INDICATORS: Dict[str, List[str]] = {
    "Module 1 — Safety & Scope Guard": [
        "app/safety/safety.py",
        "tests/test_safety*.py",
        "policies.yaml|app/safety/policies.yaml",
        "resources_in.json|app/safety/resources_in.json",
    ],
    "Module 2 — Personalization": [
        "app/personalization/",
        "app/personalization/style.py|app/personalization/stylespec.py",
        "tests/test_personalization*.py",
    ],
    "Module 3 — Conversation State Machine": [
        "app/state_machine.py|app/conversation/state_machine.py",
        "tests/test_state*.py",
    ],
    "Module 4 — Mate Mode Engine (Coach)": [
        "app/mate_mode/",
        "prompts/mate_mode.txt|prompts/mate_mode.md",
        "tests/test_mate*.py",
    ],
    "Module 5 — Inner Me Engine (Companion)": [
        "app/inner_me/",
        "prompts/inner_me_mode.txt|prompts/inner_me_mode.md",
        "tests/test_inner_me*.py",
    ],
    "Module 6 — Skills Library (Core + Advanced Packs)": [
        "app/skills/",
        "app/skills/*.py",
        "tests/test_skills*.py",
    ],
    "Module 7 — Science Notes Engine": [
        "app/science/",
        "science_catalog.json|app/science/science_catalog.json",
        "tests/test_science*.py",
    ],
    "Module 8 — Memory Layer": [
        "app/memory/",
        "app/memory/summarizer.py",
        "tests/test_memory*.py",
    ],
    "Module 9 — Knowledge & Retrieval Packs (15)": [
        "knowledge/",
        "knowledge/**/*.md",
        "app/retriever.py|app/knowledge/retriever.py",
        "tests/test_retriever*.py",
    ],
    "Module 10 — Orchestrator": [
        "app/orchestrator.py|app/orchestrator/__init__.py",
        "prompts/*.txt|prompts/*.md",
        "tests/test_orchestrator*.py",
    ],
    "Module 11 — Frontend UI (Streamlit)": [
        "Home.py|app/ui/Home.py|app/ui/home.py|home.py",
        "ui/components.py|app/ui/components.py",
        "tests/test_ui*.py",
    ],
    "Module 12 — Data Layer": [
        "app/database.py|app/db/database.py",
        "migrations/|app/db/migrations/",
        "tests/test_database*.py",
    ],
    "Module 13 — Observability & Reliability": [
        "app/logging.py|app/common/logging.py",
        "app/metrics.py|app/common/metrics.py",
        "app/cache.py|app/common/cache.py",
        "tests/test_retry*.py|tests/test_cache*.py",
    ],
    "Module 14 — Evaluation & Red-Team": [
        "tests/conversations/",
        "tests/test_adversarial*.py",
        "app/eval_runner.py|tools/eval_runner.py",
    ],
    "Module 15 — Updates & Learning Loop": [
        "knowledge_version.json|app/knowledge_version.json",
        "update_pipeline.md|docs/update_pipeline.md",
        "index_refresh.py|tools/index_refresh.py",
    ],
    "Module 16 — Accessibility & Localization": [
        "i18n/",
        "i18n/*.json",
        "tests/test_i18n*.py",
    ],
    "Module 17 — Crisis Hand-offs": [
        "safety_plan_templates/",
        "app/safety/plan_generator.py|app/safety/safety_plan.py",
        "tests/test_safety_plan*.py",
    ],
    "Module 18 — Web App (Public)": [
        "deployment/|ops/",
        "Streamlit/requirements or FastAPI/Next config markers",
        "tests/test_rate_limit*.py|tests/test_auth*.py",
    ],
    "Module 19 — Security Hardening": [
        "app/security.py|app/security/",
        "tests/test_security*.py",
    ],
    "Module 20 — Cost & Scale": [
        "budgets.yaml|config/budgets.yaml",
        "app/router.py|app/routing/router.py",
        "tests/test_router*.py|tests/test_budget*.py",
    ],
}

def _normalize_pattern(p: str) -> str:
    """
    Ensure '**' is a full segment. Convert things like '**.md' -> '**/*.md'.
    Also allows forward-slashes on Windows.
    """
    p = p.replace("\\", "/")
    # if pattern contains '**' not followed by '/', fix it
    if "**." in p:
        # e.g., 'knowledge/**.md' -> 'knowledge/**/*.md'
        p = p.replace("**.", "**/*.")
        print(f"[normalize] adjusted pattern to: {p}")
    return p

def _safe_glob(root: Path, pattern: str):
    """
    Glob with normalization and a safe fallback if pathlib complains.
    """
    try:
        patt = _normalize_pattern(pattern)
        # pathlib expects ** as full segment; this is now safe
        return list(root.glob(patt))
    except ValueError as e:
        # Fallback: manual walk if a weird pattern gets through
        print(f"[warn] bad glob '{pattern}' ({e}); falling back to walk-match")
        matches = []
        # naive suffix/prefix handling
        suffix = None
        if patt := pattern.strip():
            if patt.startswith("**/"):
                patt = patt[3:]
            if patt.startswith("./"):
                patt = patt[2:]
            if patt.endswith("/*.py"):
                suffix = ".py"
                patt = patt[:-4]
        for dirpath, dirnames, filenames in os.walk(root):
            # prune excluded dirs
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            base = Path(dirpath)
            for f in filenames:
                p = base / f
                if suffix and p.suffix == suffix:
                    matches.append(p)
        return matches

def path_exists_any(pattern: str, root: Path) -> bool:
    """
    Supports multi-option patterns separated by '|', and globs like **/*.py
    Also supports directory presence checks (pattern ending with '/').
    """
    options = [p.strip() for p in pattern.split("|")]
    for opt in options:
        if not opt:
            continue
        # directory presence check
        if opt.endswith("/"):
            pdir = (root / opt).resolve()
            if pdir.exists() and pdir.is_dir():
                return True
            # also allow without trailing slash
            pdir2 = (root / opt.rstrip("/")).resolve()
            if pdir2.exists() and pdir2.is_dir():
                return True
            # try glob as a last resort
            if _safe_glob(root, opt):
                return True
            continue

        # glob or direct file
        if any(ch in opt for ch in "*?[]"):
            if _safe_glob(root, opt):
                return True
        else:
            p = (root / opt).resolve()
            if p.exists():
                return True
    return False

def score_module(indicators: List[str], root: Path) -> Tuple[int, int]:
    hit, total = 0, len(indicators)
    for pat in indicators:
        if path_exists_any(pat, root):
            hit += 1
    return hit, total

def main() -> int:
    if not ROOT.exists():
        print("Cannot locate project root.")
        return 2

    results: List[Tuple[str, int, int]] = []
    for module_name, indicators in MODULE_INDICATORS.items():
        hit, total = score_module(indicators, ROOT)
        results.append((module_name, hit, total))

    # Write markdown report
    out = ["# MASTER_TRACKER_AUTO — Project SLUM\n"]
    out.append("| Module | Progress | Indicators |\n|---|---:|---|\n")
    for name, hit, total in results:
        pct = int(round(100 * hit / total)) if total else 0
        checkbox = "✅" if pct == 100 else ("🟡" if pct >= 50 else "⬜")
        out.append(f"| {name} | {pct}% {checkbox} | {hit}/{total} |\n")

    report = (ROOT / "MASTER_TRACKER_AUTO.md")
    report.write_text("".join(out), encoding="utf-8")

    # Console summary
    print("MASTER_TRACKER_AUTO.md written.")
    for name, hit, total in results:
        pct = int(round(100 * hit / total)) if total else 0
        print(f"- {name}: {pct}% ({hit}/{total})")

    print("\nTip: open MASTER_TRACKER_AUTO.md in VS Code and compare with MASTER_TRACKER.md.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
