# tests/test_properties_safety.py
from hypothesis import given, strategies as st
from app.safety.safety import get_safety_guard

@given(st.text(min_size=0, max_size=1000))
def test_no_crash_on_arbitrary_text(s):
    g = get_safety_guard()
    d = g.evaluate(s)
    # Always returns a valid decision with action in allowed set
    assert d.action in ("allow", "redact", "block")
