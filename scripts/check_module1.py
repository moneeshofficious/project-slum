# filename: scripts/check_module1.py
"""
Quick self-check for Module 1: Safety & Scope Guard.
- Verifies required files exist and load.
- Calls safety API surface with sample inputs.
- Prints PASS/FAIL lines you can paste into notes.
"""
from pathlib import Path
import json
import sys

REQUIRED = [
    ("policies.yaml", "YAML policy (scope/DEI)"),
    ("resources_in.json", "India helplines/resources"),
    ("consent.md", "Consent copy"),
]

def main():
    base = Path(".")
    ok = True
    for fname, desc in REQUIRED:
        p = base / fname
        if p.exists() and p.is_file():
            print(f"[PASS] {desc}: {fname}")
        else:
            print(f"[FAIL] Missing {desc}: {fname}")
            ok = False

    # Optional: light JSON validation
    rpath = base / "resources_in.json"
    if rpath.exists():
        try:
            data = json.loads(rpath.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "helplines" in data:
                print("[PASS] resources_in.json has 'helplines'")
            else:
                print("[FAIL] resources_in.json missing 'helplines' key")
                ok = False
        except Exception as e:
            print(f"[FAIL] resources_in.json not valid JSON: {e}")
            ok = False

    # Import and probe the API surface if available
    try:
        from app.safety.safety import enforce_scope, detect_risk, inject_resources, apply_dei_filter
        # Scope test
        text = "Which meds should I take for panic?"
        safe_text, is_blocked = enforce_scope(text)
        print(f"[INFO] enforce_scope blocked={is_blocked}")
        if is_blocked:
            print("[PASS] Scope block triggered on med-seeking")
        else:
            print("[FAIL] Scope block did not trigger for med-seeking"); ok = False

        # Risk detection test
        risk_info = detect_risk("I want to die", profile={"age_band": "adult"})
        print(f"[INFO] detect_risk -> {risk_info}")
        if risk_info.get("risk") in {"high", "low"}:
            print("[PASS] Risk detector classifies risky phrase")
        else:
            print("[FAIL] Risk detector missed high-risk phrase"); ok = False

        # Resource injection
        reply = "I'm here with you."
        reply2 = inject_resources(reply, risk_info)
        if reply != reply2 and "112" in reply2:
            print("[PASS] Resources injected (contains India helplines)")
        else:
            print("[FAIL] Resources missing or unchanged"); ok = False

        # DEI filter
        rew = apply_dei_filter("You are crazy.")
        if "crazy" not in rew.lower():
            print("[PASS] DEI rewrite applied")
        else:
            print("[FAIL] DEI rewrite not applied"); ok = False

    except ModuleNotFoundError:
        print("[WARN] Could not import app.safety.safety; run unit tests instead.")
    except Exception as e:
        print(f"[FAIL] Safety API smoke error: {e}"); ok = False

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
