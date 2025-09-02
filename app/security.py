from __future__ import annotations
import re

def redact_pii(text: str) -> str:
    # naive scrub for emails/phones
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[email]", text)
    text = re.sub(r"\b\d{3}[- ]?\d{3}[- ]?\d{4}\b", "[phone]", text)
    return text
