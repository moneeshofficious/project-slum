# tests/test_policy_loading_runtime.py
import os
from app.safety import config as safety_config
from app.safety.safety import enforce_scope, apply_dei_filter

def test_redirect_message_comes_from_policies_yaml():
    # The YAML we added includes the default message; assert it’s what enforce_scope uses.
    blocked, msg = enforce_scope("what dose should I take?")
    assert blocked is True
    assert "I can’t provide diagnosis or medication advice" in msg

def test_scope_patterns_from_yaml_trigger_block():
    # One of the YAML patterns is (?i)\bwhich\s+meds?\b
    blocked, _ = enforce_scope("Which meds should I take?")
    assert blocked is True

def test_dei_rewrite_uses_yaml_lexicon():
    # YAML maps 'crazy|insane' to 'feeling overwhelmed'
    out = apply_dei_filter("I feel crazy about this")
    assert "feeling overwhelmed" in out
