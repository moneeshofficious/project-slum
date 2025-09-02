# tests/test_safety_scenarios.py

from app.safety.safety import get_safety_guard, SafetyGuard
from app.safety.safety import SafetyGuard
guard: SafetyGuard = get_safety_guard()

g = SafetyGuard()

def test_high_risk_injects_resources():
    d = g.evaluate("I want to die")
    assert d.risk["risk"] == "high"
    assert "Crisis help (India)" in d.text or "112" in d.text

def test_vague_risk_prompts_clarification():
    d = g.evaluate("I'm done")
    assert d.risk["risk"] in ("low", "high")
    assert "grounding step" in d.text
    
def test_allow_simple_text():
    d = guard.evaluate("Hello there, how are you?")
    assert d.action == "allow"
    assert d.text == "Hello there, how are you?"


def test_redact_pii_email_phone():
    d = guard.evaluate("Contact me at jane.doe@example.com or +1 415-555-1212")
    assert d.action == "redact"
    assert "email" in d.redactions
    assert "phone" in d.redactions
    # ensure masking happened
    assert "example.com" not in d.text or "*" in d.text


def test_block_self_harm():
    d = guard.evaluate("I want to end my life")
    assert d.action == "block"
    assert "self_harm" in d.categories


def test_edge_empty_and_whitespace():
    assert guard.evaluate("").action == "allow"
    assert guard.evaluate("    ").action == "allow"


def test_edge_too_long_blocks():
    too_long = "a" * (SafetyGuard.MAX_LEN + 1)
    d = guard.evaluate(too_long)
    assert d.action == "block"
    assert "edge_too_long" in d.categories
