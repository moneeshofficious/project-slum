# app/security/security.py
# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import Optional, Callable

try:
    # Prefer Safety so both layers emit SAME tokens:
    #   [redacted@email], [redacted phone]
    from app.safety.safety import redact_pii as _safety_redact_pii  # type: ignore
except Exception:  # pragma: no cover
    _safety_redact_pii = None  # type: Optional[Callable[[Optional[str]], Optional[str]]]

from app.metrics.counters import redactions_total

_EMAIL_TOKEN = "[redacted@email]"
_PHONE_TOKEN = "[redacted phone]"

# Minimal fallback regexes if Safety import is unavailable
_FALLBACK_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_FALLBACK_PHONE_RE = re.compile(r"(?<!\w)\+?\d{1,3}(?:[\s.\-]*\d{2,4}){2,4}(?!\w)")

def _fallback_redact_pii(text: Optional[str]) -> Optional[str]:
    """Fallback redactor used only when Safety is not available.
    Increments metrics here to avoid double-counting when Safety is present.
    """
    if text is None or text == "":
        return text

    # Emails
    def _email_sub(_: re.Match) -> str:
        return _EMAIL_TOKEN
    redacted_email, n_email = _FALLBACK_EMAIL_RE.subn(_email_sub, text)

    # Phones
    def _phone_sub(m: re.Match) -> str:
        s = m.group(0).strip()
        return ("+" if s.startswith("+") else "") + _PHONE_TOKEN
    redacted_all, n_phone = _FALLBACK_PHONE_RE.subn(_phone_sub, redacted_email)

    if n_email:
        redactions_total().labels(kind="email").inc(n_email)
    if n_phone:
        redactions_total().labels(kind="phone").inc(n_phone)

    return redacted_all

def redact(text: Optional[str]) -> Optional[str]:
    """Public security-layer redactor. Delegates to Safety when available."""
    if _safety_redact_pii is not None:
        # Safety may handle its own metrics; do not double-count here.
        return _safety_redact_pii(text)
    return _fallback_redact_pii(text)

def redact_pii(text: Optional[str]) -> Optional[str]:
    """Alias for callers that still import redact_pii from security."""
    return redact(text)

__all__ = ["redact", "redact_pii"]
