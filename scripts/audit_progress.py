# filename: scripts/audit_progress.py
"""
Project SLUM — Progress Audit
- Prints file presence for core Phase 1 items.
- Runs pytest and shows a short summary.
- Exits 0 if all good, 1 if something needs attention.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(".").resolve()

REQUIRED_FILES = [
    # Module 1 data model & files
    ("policies.yaml", "Module 1 policy file"),
    ("resources_in.json", "Module 1 India helplines"),
    ("consent.md", "Module 1 consent copy"),
    # Module 1 code + packages
    ("app/__init__.py", "app package"),
    ("app/safety/__init__.py", "app.safety package"),
    ("app/safety/safety.py", "safety APIs"),
    # Tests and scripts
    ("scripts/check_module1.py", "Module 1 self-check script"),
    ("tests/test_safety_unit.py", "Unit tests for safety"),
    ("tests/test_safety_scenarios.py", "Scenario tests for safety"),
    ("tests/test_safety_adversarial.py", "Adversarial/edge tests for safety"),
]

def check_files():
    print("\n== File presence check ==")
    ok = True
    for rel, label in REQUIRED_FILES:
        p = ROOT / rel
        if p.exists():
            print(f"[PASS] {label}: {rel}")
        else:
            print(f"[FAIL] Missing {label}: {rel}")
            ok = False
    return ok

def run_pytest():
    print("\n== Test run ==")
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        print(r.stdout)
        if r.returncode == 0:
            print("[PASS] Pytest passed")
            return True
        else:
            print("[FAIL] Pytest failed")
            print(r.stderr)
            return False
    except Exception as e:
        print(f"[FAIL] Could not run pytest: {e}")
        return False

def main():
    files_ok = check_files()
    tests_ok = run_pytest()
    all_ok = files_ok and tests_ok
    print("\n== Summary ==")
    if all_ok:
        print("[GREEN] Project baseline looks good.")
        sys.exit(0)
    else:
        print("[RED] Some checks failed. See FAIL lines above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
