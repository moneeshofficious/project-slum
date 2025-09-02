# tests/test_redaction_tokens.py
import pytest
from app.safety.safety import redact_pii
from app.security.security import redact as sec_redact

CASES = [
    "Email me at a.b+c@ex.co",
    "Call me at +1 415-555-1234",
    "Or dial 040-1234-5678",
]

@pytest.mark.parametrize("s", CASES)
def test_tokens_consistent(s):
    out1 = redact_pii(s)
    out2 = sec_redact(s)
    assert "[redacted@email]" in out1 or "[redacted phone]" in out1
    assert out1 == out2
