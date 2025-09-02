from app.safety.safety import needs_consent, record_consent
from app.data.database import init_db

def test_consent_persists():
    init_db()
    uid = "test_user_123"
    assert needs_consent(uid) is True
    record_consent(uid)
    assert needs_consent(uid) is False