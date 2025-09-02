# tests/test_safety_coverage.py
import base64

from app.safety.safety import SafetyGuard, enforce_scope, apply_dei_filter

def test_control_chars_removed_and_flagged():
    g = SafetyGuard()
    d = g.evaluate("hi\x00there")
    assert "edge_control_chars" in d.categories
    assert "\x00" not in d.text

def test_repeat_spam_flag():
    g = SafetyGuard()
    d = g.evaluate("a" * 60)
    assert "edge_repeat_spam" in d.categories

def test_base64_blob_flag_only():
    g = SafetyGuard()
    blob = base64.b64encode(b"x" * 200).decode()
    d = g.evaluate(blob)
    # Should not crash and should tag as base64-ish
    assert "edge_base64_blob" in d.categories

def test_long_text_is_blocked():
    g = SafetyGuard()
    d = g.evaluate("x" * 20000)
    assert d.action == "block"
    assert "edge_too_long" in d.categories

def test_address_hint_counts_as_pii_note():
    g = SafetyGuard()
    d = g.evaluate("I live on MG road near the district office, flat 12B")
    # No masking, but we note an address hint under PII
    assert "pii" in d.categories
    assert d.redactions.get("address_hint", 0) >= 1

def test_emoji_only_is_allowed_noop():
    g = SafetyGuard()
    d = g.evaluate("🙂🙂🙂")
    assert d.action in ("allow", "redact", "block")  # sanity
    # We at least ensure no crash and it passes through as non-blocking
    assert d.action != "block"

def test_whitespace_only_allowed():
    g = SafetyGuard()
    d = g.evaluate("   \n\t  ")
    # Should be a benign pass-through (not a block)
    assert d.action != "block"

def test_dei_filter_rewrites_stigmatizing_terms():
    out = apply_dei_filter({"sections": {"reflect": "I feel crazy and mentally ill lately"}})
    text = out["sections"]["reflect"]
    assert "crazy" not in text.lower()
    assert "mentally ill" not in text.lower()
    assert "feeling overwhelmed" in text.lower()
    assert "person living with a mental health condition" in text.lower()

def test_scope_redirect_message_contains_key_phrase():
    blocked, msg = enforce_scope("Which meds should I take for anxiety?")
    assert blocked is True
    assert "I can’t provide diagnosis or medication advice" in msg
