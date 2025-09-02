# tools/eval_runner.py
"""
Simple Evaluation Runner
- Loads golden dialogs from tests/conversations/*.json
- Applies lightweight checks (forbidden content flags, must-include strings)
- Writes eval_results.md with pass/fail
Run:
  (.venv) PS> python tools/eval_runner.py
"""
from __future__ import annotations
import json, glob, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLDEN_DIR = ROOT / "tests" / "conversations"
OUT = ROOT / "eval_results.md"

def evaluate_item(item: dict) -> list[str]:
    errors = []
    expected = item.get("expected_contains") or []
    forbidden = item.get("forbidden_contains") or []
    response = item.get("response", "")
    for must in expected:
        if must not in response:
            errors.append(f"Missing expected: {must!r}")
    for bad in forbidden:
        if bad in response:
            errors.append(f"Contains forbidden: {bad!r}")
    return errors

def load_cases() -> list[dict]:
    cases = []
    for path in glob.glob(str(GOLDEN_DIR / "*.json")):
        try:
            obj = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
            if isinstance(obj, list):
                cases.extend(obj)
            elif isinstance(obj, dict):
                cases.append(obj)
        except Exception as e:
            cases.append({"id": path, "response": "", "expected_contains": [], "forbidden_contains": ["__PARSE_ERROR__"], "note": str(e)})
    return cases

def main() -> int:
    cases = load_cases()
    passed, failed = 0, 0
    lines = ["# Evaluation Results\n\n"]
    for i, c in enumerate(cases, 1):
        errs = evaluate_item(c)
        if errs:
            failed += 1
            lines.append(f"## Case {i} — ❌ FAIL\n- id: {c.get('id','(no id)')}\n- errors:\n" + "".join(f"  - {e}\n" for e in errs) + "\n")
        else:
            passed += 1
            lines.append(f"## Case {i} — ✅ PASS\n- id: {c.get('id','(no id)')}\n\n")
    lines.append(f"\n**Summary:** {passed} passed / {failed} failed / total {len(cases)}\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"eval_results.md written. {passed} pass / {failed} fail.")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
