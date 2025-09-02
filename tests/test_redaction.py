# tests/test_redaction.py
from app.security.security import redact_pii

def test_redact_email_phone():
    s = "Email me at jane.doe@example.com or call +1 415-555-1234 today."
    out = redact_pii(s)
    assert "[redacted@email]" in out
    assert "[redacted phone]" in out
