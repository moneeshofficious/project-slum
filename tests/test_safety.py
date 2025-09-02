# tests/test_safety.py
from app.safety.safety import enforce_scope, detect_risk, apply_dei_filter, inject_resources

def test_scope_block():
    blocked, msg = enforce_scope("Can you prescribe meds?")
    assert blocked is True
    assert "I can’t provide diagnosis or medication advice" in msg

def test_risk_detects_high():
    info = detect_risk("I want to end my life", profile={"country": "IN"})
    assert info["risk"] == "high"
    assert any("keyword" in r for r in info["reasons"])

def test_dei_rewrite():
    reply = {"sections": {"reflect": "I feel crazy lately"}}
    out = apply_dei_filter(reply)
    assert "overwhelmed" in out["sections"]["reflect"].lower()

def test_inject_resources_on_high_risk():
    reply = {"sections": {"validate": "Thanks for sharing"}}
    info = {"risk": "high", "reasons": ["keyword:suicide"], "soft_prompt": "Support prompt"}
    out = inject_resources(reply, info)
    assert "resources" in out
    assert out.get("meta", {}).get("risk_resources_shown") is True
