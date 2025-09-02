# app/security/__init__.py
"""
Security package exposing redact_pii for tests and utilities.
"""
from .security import redact_pii

__all__ = ["redact_pii"]
