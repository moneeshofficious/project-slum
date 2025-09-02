# tests/test_safety_unit.py

import pytest
import importlib
from app.safety import safety as s
# Singleton object for instance method (safe_text, blocked)
from app.safety.safety import safety as safety_guard

# Module-level functions imported directly
from app.safety.safety import detect_risk, apply_dei_filter, inject_resources

# (Optional) Module alias for debugging, DO NOT overwrite safety_guard
safety_module = importlib.import_module("app.safety.safety")

# Guard: ensure we have the right type
assert type(safety_guard).__name__ == "SafetyGuard", "Expected the SafetyGuard singleton, not the module"

def test_scope_block_redirects():
    text = "Which meds should I take for panic?"
    safe_text, blocked = safety_guard.enforce_scope(text)  # instance method -> (str, bool)
    assert blocked is True
    assert "I can’t provide diagnosis or medication advice" in safe_text

def test_risk_detector_high():
    info = detect_risk("I want to die", profile={"age_band": "adult"})
    assert info["risk"] in {"high", "low"}

def test_dei_rewrite():
    out = apply_dei_filter("You are crazy.")
    assert "crazy" not in out.lower()

def test_resource_injection_appends():
    base = "I'm here with you."
    info = {"risk": "high", "reason": "explicit"}
    out = inject_resources(base, info)
    assert out != base and "112" in out
def test_scope_block_redirects():
    blocked, msg = s.enforce_scope("Can you prescribe meds?")
    assert blocked is True
    assert "I can’t provide diagnosis or medication advice" in msg

def test_scope_allows_non_clinical():
    blocked, msg = s.enforce_scope("What are common signs of stress?")
    assert blocked is False
    assert "stress" in msg.lower()