# app/safety/__init__.py
# Re-export public API so tests can import from `app.safety`
from .safety import (
    safety,
    get_safety_guard,
    enforce_scope,
    detect_risk,
    apply_dei_filter,
    inject_resources,
    pre_prompt_guard,
    post_prompt_guard,
    refresh_policies,
    needs_consent,
    record_consent,
    redact_pii,
    redact,
    _METRICS,  # back-compat for tests
)

__all__ = [
    "safety",
    "get_safety_guard",
    "enforce_scope",
    "detect_risk",
    "apply_dei_filter",
    "inject_resources",
    "pre_prompt_guard",
    "post_prompt_guard",
    "refresh_policies",
    "needs_consent",
    "record_consent",
    "redact_pii",
    "redact",
    "_METRICS",
]
